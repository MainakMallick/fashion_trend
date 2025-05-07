from playwright.sync_api import sync_playwright
import time

def scrape_pinterest_trends(query="streetwear", scrolls=3):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        search_url = f"https://www.pinterest.com/search/pins/?q={query}"
        page.goto(search_url, timeout=60000)
        time.sleep(5)

        for _ in range(scrolls):
            page.mouse.wheel(0, 3000)
            time.sleep(2)

        pins = page.query_selector_all("div[data-test-id='pin']")

        results = []
        for pin in pins[:30]:  # Limit results
            try:
                title = pin.inner_text()
                image = pin.query_selector("img").get_attribute("src")
                results.append({
                    "title": title.strip()[:100],
                    "image": image
                })
            except:
                continue

        browser.close()
        return results

# Example usage:
if __name__ == "__main__":
    data = scrape_pinterest_trends("minimalist fashion")
    for d in data:
        print(d["title"])
        print(d["image"])
        print("------")
