import numpy as np
from scraper.db import get_database
import seaborn as sns
import matplotlib.pyplot as plt
from mood.dashboard.utils import get_scores_per_category_and_tab, get_most_active_categories
from scraper.constants import TABS
import os

def calcuate_percentiles(db):
    print(db.list_collection_names())
    for category in db.list_collection_names():
        print(f"Stats for {category}")
        for tab in TABS:
            print(f"IN TOP: {tab}")
            scores = [
                doc['trend_score']
                for doc in db[category].find({'top_type': tab}, {'trend_score': 1})
            ]
            mean = 0
            std = 0
            p85 = 0
            if scores:
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

def trend_score_distribution(db):
    os.makedirs("plots", exist_ok=True)
    data = get_scores_per_category_and_tab(db)
    for category, apps in data.items():
        for tab in TABS:
            scores = apps[tab]
            if scores:
                filename = f"{category}_{tab}.png"
                plt.figure(figsize=(10, 6))
                sns.histplot(scores, bins=50, kde=True)
                title = f'Threshold distribution in {category}, {tab}'
                plt.axvline(x=25, color='red', linestyle='--', label='Current threshold')
                plt.xlabel("Trend Score")
                plt.ylabel("App count")
                plt.title(title)
                plt.legend()

                output_path = os.path.join("plots", filename)
                plt.savefig(output_path)
                plt.close()
                print(f"Saved: {filename}")

    print("All plots saved!")

def main():
    db = get_database()
    trend_score_distribution(db)

if __name__ == "__main__":
    main()
