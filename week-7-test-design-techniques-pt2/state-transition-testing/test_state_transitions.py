import pytest
from playwright.sync_api import expect, sync_playwright


def login_helper(p):
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.goto("https://parabank.parasoft.com/parabank/index.htm")
    page.fill('input[name="username"]', "john")
    page.fill('input[name="password"]', "demo")
    page.click('input[value="Log In"]')

    return page, browser


def test_loan_submission_moves_to_processed_and_outcome():
    """
    This test follows the conceptual state machine in the diagram:

        LoanForm → Loan Request Processed → Approved/Denied → LoanAccountCreated (if approved)

    BUT ParaBank compresses two states ("Processed" + "Outcome") into one screen,
    and sometimes crashes instead of showing "Denied".

    This test handles both the intended workflow AND the real system behaviour.
    """

    with sync_playwright() as p:
        page, browser = login_helper(p)

        # --- STATE: LoanForm ---
        # Diagram: User is authenticated and sees the loan form.
        expect(page.get_by_role("heading", name="Accounts Overview")).to_be_visible()

        page.click('a[href*="requestloan"]')
        expect(page.get_by_role("heading", name="Apply for a Loan")).to_be_visible()

        # ParaBank has no labels or IDs, so we select textboxes by index.
        amount_input = page.get_by_role("textbox").nth(0)
        downpayment_input = page.get_by_role("textbox").nth(1)

        amount_input.fill("1000")
        downpayment_input.fill("100")

        page.get_by_role("combobox").select_option(index=0)

        # --- TRANSITION: LoanForm → Processed ---
        page.get_by_role("button", name="Apply Now").click()

        # Check for crash first (real system behaviour)
        if page.locator("text=Error!").is_visible():
            # Diagram: This is NOT a valid state. It's a system failure.
            assert (
                False
            ), "System crashed instead of reaching 'Loan Request Processed' state."

        # --- STATE: Loan Request Processed ---
        # Diagram: This should always appear after submission.
        expect(page.locator("text=Loan Request Processed")).to_be_visible()

        # --- TRANSITION: Processed → Outcome ---
        # Diagram: System evaluates → Approved OR Denied
        expect(page.locator("text=Status")).to_be_visible()

        status_text = page.locator("text=Status").inner_text()

        # --- STATE: Approved OR Denied ---
        # Diagram: Branching logic
        page.click("a[href*='overview']")

        if "Approved" in status_text:
            # --- TRANSITION: Approved → LoanAccountCreated ---
            # Diagram: Loan account should be created
            expect(page.locator("text=Loan Account")).to_be_visible()

        else:
            # --- TRANSITION: Denied → Terminal ---
            # Diagram: No loan account should exist
            expect(page.locator("text=Loan Account")).not_to_be_visible()

        browser.close()
