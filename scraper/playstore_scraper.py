from google_play_scraper import search


TABS = {
    "top_free": "Top free",
    "top_grossing": "Top grossing",
    "top_paid": "Top paid"
}

def scrape_play_store_search(search_term: str):
    result = search(
        search_term,
        lang='en',
        country='us',
        n_hits=4,
    )
    return result

async def category(filter, url, page):
    print(f"Navigating to {url}")
    await page.goto(url, {'waitUntil': 'networkidle2'})
    await page.waitForSelector('div[role="tablist"]')

    results = {}

    for tab_name, aria_label in TABS.items():
        print(f"\nScraping tab: {tab_name}")
        
        await page.evaluate('window.scrollTo(0, 0);')

        tab_selector = f'div[role="button"][aria-label="{aria_label}"]'
        await page.waitForSelector(tab_selector, {'visible': True})
        await page.querySelectorEval(tab_selector, 'el => el.click()')
        await page.waitFor(3000)

        # Wait for the app grid to appear
        try:
            await page.waitForSelector('a[href*="/store/apps/details?id="]')

            # Evaluate and extract links
            links = await page.evaluate('''() => {
                const anchors = Array.from(document.querySelectorAll('a[href*="/store/apps/details?id="]'));
                const urls = anchors.map(a => a.href);
                //return [...new Set(urls)];  // Deduplicate
                return urls
            }''')

            print(f"Found {len(links)} apps.")
        except TimeoutError:
            print("Selector not found, returning empty list")
            links = []
        results[tab_name] = links[filter:]

    return results

