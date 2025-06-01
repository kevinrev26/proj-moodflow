from .constants import category_list
import asyncio, random
from pyppeteer import launch
from config.settings import PUPPETEER_CONFIG
from .playstore_scraper import category
import json

BASE_CATEGORY_URL = "https://play.google.com/store/apps/category/"

async def get_playstore_urls():
    leaderboard = {}
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

    with open('leaderboard.json', 'w') as file:
        json.dump(leaderboard, file, indent=4)
    
    print("Finished! file created")

if __name__ == "__main__":
    asyncio.run(get_playstore_urls())
