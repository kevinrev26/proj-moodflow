from constants import Category
from playstore_scraper import category
import asyncio
import pprint

def get_playstore_urls():
    results = asyncio.run(category(Category.ART))
    print(results)


if __name__ == "__main__":
    get_playstore_urls()
