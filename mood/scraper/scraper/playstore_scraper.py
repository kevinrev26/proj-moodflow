from google_play_scraper import search
# import requests
# from bs4 import BeautifulSoup
from urllib.parse import urljoin
# import asyncio
from pyppeteer import launch
# from typing import Dict, List

BASE_CATEGORY_URL = "https://play.google.com/store/apps/category/"

TABS = {
    "Top free": "Top free",
    "Top grossing": "Top grossing",
    "Top paid": "Top paid"
}

def scrape_play_store_search(search_term: str):
    result = search(
        search_term,
        lang='en',
        country='us',
        n_hits=4,
    )
    return result

async def category(category: str, lang: str = "en", country: str = "us"):
    url = BASE_CATEGORY_URL + category

    browser = await launch(
        headless=True,
        executablePath='/home/kevinrev26/.local/share/pyppeteer/local-chromium/1181205/chrome-linux/chrome',
        args=[
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-gpu',
            '--disable-dev-shm-usage',
            '--no-zygote',
            '--single-process',
            '--disable-extensions',
        ],
        autoClose = False
    )
    page = await browser.newPage()
    print(f"Navigating to {url}")
    await page.goto(url, {'waitUntil': 'networkidle2'})
    await page.waitForSelector('div[role="tablist"]')

    results = {}

    for tab_name, aria_label in TABS.items():
        print(f"\nScraping tab: {tab_name}")
        
        await page.evaluate('window.scrollTo(0, 0);')

        tab_selector = f'div[role="button"][aria-label="{aria_label}"]'
        await page.waitForSelector(tab_selector, {'visible': True})
        print("Waiting for tab selector")
        await page.querySelectorEval(tab_selector, 'el => el.click()')
        print("Clicking on tab element")
        await page.waitFor(3000)
        print("Content should be loaded")
        # await page.waitForTimeout(3000)  # Wait for async content to load

        # Wait for the app grid to appear
        await page.waitForSelector('a[href*="/store/apps/details?id="]')

        # Evaluate and extract links
        links = await page.evaluate('''() => {
            const anchors = Array.from(document.querySelectorAll('a[href*="/store/apps/details?id="]'));
            const urls = anchors.map(a => a.href);
            //return [...new Set(urls)];  // Deduplicate
            return urls
        }''')

        print(f"Found {len(links)} apps.")
        results[tab_name] = links[20:]

    await browser.close()
    return results

    # print(BASE_URL)
    # response = requests.get(BASE_URL)
    # soup = BeautifulSoup(response.text, "html.parser")
    # links = soup.find_all("a", href=True)

    # public_urls = set()

    # with open('play.html', '+a') as html_file:
    #     html_file.write(response.text)
    #     print('Done!')

    # for link in links:
    #     href = link['href']
    #     if href.startswith("/store/apps/details"):
    #         full_url = urljoin(BASE_URL, href)
    #         public_urls.add(full_url)

    # # Print unique public URLs
    # print("\n📎 Discovered Public URLs:")
    # for url in sorted(public_urls):
    #     print(url)
