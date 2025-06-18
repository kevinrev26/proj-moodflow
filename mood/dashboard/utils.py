from scraper.constants import MIN_ACTIVE_APPS, TABS
import numpy as np
import pandas as pd

def is_active_category(category, tab, db, trend_threshold):
    #TODO Documentation
    active_apps = db[category].distinct(key='app_id', filter={'trend_score': {'$gt': trend_threshold}, 'top_type': tab})
    return len(list(active_apps)) >= MIN_ACTIVE_APPS

def get_scores_per_category_and_tab(db):
    #TODO Doc
    data = {}
    for category in db.list_collection_names():
        data[category] = {}
        for tab in TABS:
            scores = [
                doc['trend_score']
                for doc in db[category].find({'top_type': tab}, {'trend_score': 1})
            ]
            data[category][tab] = scores

    return data

def get_most_active_categories(percentiles):
    percentile_85_scores = []

    for category, tops in percentiles.items():
        for top_type, values in tops.items():
            p85 = values[1]
            percentile_85_scores.append(((category, top_type), p85))
    
    df = pd.DataFrame([
        {"category": cat, "top_type": top, "p85": p85}
        for (cat, top), p85 in percentile_85_scores
    ])

    df_sorted = df.sort_values(by="p85", ascending=False).reset_index(drop=True)
    top_categories = (
        df_sorted.drop_duplicates(subset='category', keep='first')
        .head(5)['category'].tolist()
    )
    return top_categories

def get_percentiles(db):
    data = get_scores_per_category_and_tab(db)
    percentiles = {}
    for category, apps in data.items():
        percentiles[category] = {}
        for tab in TABS:
            scores = apps[tab]
            if scores:
                percentiles[category][tab] = np.percentile(scores, [75, 85, 90])

    return percentiles

def get_top_apps(db, top=5):
    highest_scores = []
    for category in db.list_collection_names():
        app = list(db[category].find({'trend_score': {'$gt':0}}).sort("trend_score").limit(1))[0]
        del app['_id']
        highest_scores.append(app)
    sorted_apps = sorted(highest_scores, key=lambda x: x['trend_score'], reverse=True)
    return sorted_apps[:top]

def find_app_by_id(db, app_id):
    for category in db.list_collection_names():
        doc = db[category].find_one({'app_id': app_id})
        if doc:
            return doc
    return None

