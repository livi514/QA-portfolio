from playwright.sync_api import expect, sync_playwright


def login_helper(p):
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.goto("https://parabank.parasoft.com/parabank/index.htm")
    page.fill('input[name="username"]', "john")
    page.fill('input[name="password"]', "demo")
    page.click('input[value="Log In"]')

    return page, browser


def test_loan_submission_moves_to_submitted():
    with sync_playwright() as p:
        page, browser = login_helper(p)

        expect(page.get_by_role("heading", name="Accounts Overview")).to_be_visible()

        page.click('a[href*="requestloan"]')

        # Wait for the form by checking the heading
        expect(page.get_by_role("heading", name="Apply for a Loan")).to_be_visible()

        # Select the inputs by index (ParaBank has no labels)
        amount_input = page.get_by_role("textbox").nth(0)
        downpayment_input = page.get_by_role("textbox").nth(1)

        amount_input.fill("1000")
        downpayment_input.fill("100")

        page.get_by_role("combobox").select_option(index=0)

        page.get_by_role("button", name="Apply Now").click()

        expect(page.locator("text=Loan Request Processed")).to_be_visible()
        expect(page.locator("text=Status")).to_be_visible()

        browser.close()
