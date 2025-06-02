import numpy as np
from scraper.db import get_database

def calcuate_percentiles(db):
    print(db.list_collection_names())
    for category in db.list_collection_names():
        print(f"Stats for {category}")
        scores = [doc['trend_score'] for doc in db[category].find({}, {'trend_score': 1})]
        mean = np.mean(scores)
        std = np.std(scores)
        _, p85, _ = np.percentile(scores, [75, 85, 90])
        if p85 > 9:
            print("🔥 Trending Apps")
        elif mean < -5 and p85 == 0:
            print("📉 Apps crashing")
        elif abs(mean) < 3 and std < 5:
            print("💤 Stable category")
        else:
            print("📊 No relevant changes")

def main():
    db = get_database()
    calcuate_percentiles(db)

if __name__ == "__main__":
    main()