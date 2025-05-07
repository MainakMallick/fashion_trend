from playwright.sync_api import sync_playwright
import json

def scrape(query="streetwear", scrolls=2):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(f"https://www.pinterest.com/search/pins/?q={query}", timeout=60000)

        for _ in range(scrolls):
            page.mouse.wheel(0, 3000)
        page.wait_for_timeout(2000)

        pins = page.query_selector_all("div[data-test-id='pin']")
        results = []
        for pin in pins[:30]:
            try:
                title = pin.inner_text()
                image = pin.query_selector("img").get_attribute("src")
                results.append({"title": title[:100], "image": image})
            except:
                continue
        browser.close()

        with open("scraped_data.json", "w") as f:
            json.dump(results, f, indent=2)

if __name__ == "__main__":
    scrape()
