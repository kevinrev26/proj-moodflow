from .constants import category_list
import asyncio, random
from pyppeteer import launch
from config.settings import PUPPETEER_CONFIG, MISC_CONFIG
from .playstore_scraper import category
from .db import get_database
from google_play_scraper import app
from datetime import datetime, timezone

SIGNIFICANT_CHANGE = 5

BASE_CATEGORY_URL = "https://play.google.com/store/apps/category/"

async def get_playstore_urls():
    leaderboard = {}
    now = datetime.now(timezone.utc)
    print(f"Scrapper is running at {now}")
    print("Openning browser session")
    browser = await launch(
        headless=True,
        executablePath=PUPPETEER_CONFIG['executablePath'],
        args=PUPPETEER_CONFIG['args'],
        autoClose = PUPPETEER_CONFIG['autoClose']
    )
    page = await browser.newPage()
    print("Browser created")

    for obj in category_list:
        leaderboard[obj.name] = await category(obj.filter, BASE_CATEGORY_URL+obj.name, page)
        await_time = random.uniform(6, 10)
        print(f'Awaiting {await_time} seconds before star new operation')
        await asyncio.sleep(await_time)
    
    print("Closing browser session")
    await browser.close()

    data = format_app_ids(leaderboard)
    print("Getting database client!")
    db = get_database()
    elapsed = 6
    filename = MISC_CONFIG['LAST_RUN_PATH']
    try:
        with open(filename, "r") as f:
            last_time = datetime.fromisoformat(f.read().strip())
    except (FileNotFoundError, ValueError):
        last_time = None

    if last_time:
        elapsed = (now - last_time).total_seconds() / 3600
    
    print(f"{elapsed} hours have passed since last run")
    process_leaderboard_json(db, data, elapsed)
    with open(filename, "w") as f:
        f.write(now.isoformat())
    print("Finished! Database updated")

def format_app_ids(datum: dict):
    result = {}

    for category, rank_types in datum.items():
        result[category] = {}

        for ranking_type, app_urls in rank_types.items():
            ranked_apps = []
            for rank, url in enumerate(app_urls):
                if 'id=' in url:
                    app_id = url.split('id=')[-1].strip()
                    ranked_apps.append({
                        "app_id": app_id,
                        "rank": rank + 1
                    })
            result[category][ranking_type] = ranked_apps

    return result

def calculate_trends(old_rank, new_rank, hours_elapsed, old_ratings, new_ratings, score):
    delta_rank = old_rank - new_rank
    velocity = delta_rank / hours_elapsed if hours_elapsed > 0 else 0
    rating_growth = ((new_ratings - old_ratings) / old_ratings) * score if old_ratings and old_ratings > 0 else 0

    trend_score = 1.0 * delta_rank + 2.0 * velocity + 3.0 * rating_growth
    return trend_score


def process_leaderboard_json(db, leaderboard_data, hours_elapsed=6):
    for category, top_dict in leaderboard_data.items():
        collection = db[category]
        print(f"Processing: {category}")
        for top_type, apps in top_dict.items():
            count = len(apps)
            print(f"Processing {count} apps...")
            for app_entry in apps:
                app_id = app_entry['app_id']
                current_rank = app_entry['rank']
                now = datetime.now(timezone.utc)

                existing = collection.find_one({"app_id": app_id, "top_type": top_type})

                if existing:
                    previous_rank = existing.get('current_rank', current_rank)
                    trend_score = existing.get('trend_score', 1)
                    if abs(previous_rank - current_rank) >= SIGNIFICANT_CHANGE:
                        try:
                            metadata = app(app_id)
                            new_ratings = metadata.get('ratings', existing.get('ratings', 1))
                            score = metadata.get('score', existing.get('score', 0))
                        except Exception as e:
                            print(f"Scraping error for {app_id}: {e}")
                            new_ratings = existing.get('ratings', 1)
                            score = existing.get('score', 0)

                        trend_score = calculate_trends(
                            old_rank=previous_rank,
                            new_rank=current_rank,
                            hours_elapsed=hours_elapsed,
                            old_ratings=existing.get('ratings', 1),
                            new_ratings=new_ratings,
                            score=score
                        )

                        collection.update_one(
                            {"_id": existing["_id"]},
                            {"$set": {
                                "previous_rank": previous_rank,
                                "current_rank": current_rank,
                                "last_updated": now,
                                "ratings": new_ratings,
                                "score": score,
                                "trend_score": trend_score
                            }}
                        )
                else:                    
                    try:
                        metadata = app(app_id)
                        new_doc = {
                            "app_id": app_id,
                            "title": metadata.get('title'),
                            "installs": metadata.get('installs'),
                            "score": metadata.get('score'),
                            "ratings": metadata.get('ratings'),
                            "top_type": top_type,
                            "category": category,
                            "previous_rank": current_rank,
                            "current_rank": current_rank,
                            "first_seen": now,
                            "last_updated": now,
                            "trend_score": 0.0
                        }
                        collection.insert_one(new_doc)
                    except Exception as e:
                        print(f"Error scraping {app_id}: {e}")

if __name__ == "__main__":
    asyncio.run(get_playstore_urls())
