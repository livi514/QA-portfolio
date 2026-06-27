from playwright.sync_api import sync_playwright

# 
def test_title():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("https://www.saucedemo.com/")
        assert "Swag Labs" in page.title()
        browser.close()
