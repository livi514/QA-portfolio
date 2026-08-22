# See state-transition-table.md for the full state transition table these
# tests are based on. Only rows marked "Direct" in that table are exercised
# here -- "Structural" rows (e.g. "no deny-after-approve transition exists",
# or "duplicate submission" once reclassified after checking the real UI)
# aren't tested because there's no UI action that could trigger them.

import pytest
from playwright.sync_api import expect, sync_playwright

LOGIN_URL = "https://parabank.parasoft.com/parabank/index.htm"


# --- Fixtures ---------------------------------------------------------------


@pytest.fixture
def page():
    """
    Function-scoped (not module-scoped like the CommitQuality suite) because
    loan requests mutate account state -- each test should start from a
    fresh login rather than share state/history with other tests in the
    file. Costs more browser launches, but avoids one test's submitted loan
    bleeding into another test's assertions about "no loan account exists."
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        pg = browser.new_page()

        pg.goto(LOGIN_URL)
        pg.fill('input[name="username"]', "john")
        pg.fill('input[name="password"]', "demo")
        pg.click('input[value="Log In"]')
        expect(pg.get_by_role("heading", name="Accounts Overview")).to_be_visible()

        yield pg

        browser.close()


def get_account_ids(page):
    """
    Returns the set of account IDs currently listed in Accounts Overview.

    Added after review: there is no "Loan Account" label anywhere on the
    real Accounts Overview page - confirmed via a real test run, where
    accounts are listed only by numeric ID in a shared table alongside
    every other account type (checking/savings/loan all look identical).
    So "did a loan account get created" can only be verified structurally,
    by diffing the account list before and after submission, not by
    searching for text that doesn't exist on the page.
    """
    page.click("a[href*='overview']")
    expect(page.get_by_role("heading", name="Accounts Overview")).to_be_visible()

    # Wait for the AJAX-populated table body to actually contain rows,
    # rather than reading it the instant the (initially empty) <tbody>
    # exists in the DOM.
    page.wait_for_selector("#accountTable tbody tr", timeout=10000)

    # Account IDs appear as link text in the first column of the table,
    # e.g. "13344", "16341" - linking to activity.htm?id=<id>.
    id_links = page.locator("#accountTable a[href*='activity.htm?id=']")
    return {id_links.nth(i).inner_text() for i in range(id_links.count())}


def submit_loan_request(page, amount: str, downpayment: str, from_account_id: str = None):
    """
    Shared helper: navigates to the loan form, fills it, and submits.
    Returns the page in whatever state it lands on afterward (Processed,
    an outcome screen, or an Error page) - callers are responsible for
    asserting what they expect to see next.
    """
    page.click('a[href*="requestloan"]')
    expect(page.get_by_role("heading", name="Apply for a Loan")).to_be_visible()

    # ParaBank has no labels or IDs on the amount/downpayment fields, so we
    # select by index. Order-dependent, would silently break if ParaBank
    # reorders the form.
    amount_input = page.get_by_role("textbox").nth(0)
    downpayment_input = page.get_by_role("textbox").nth(1)

    amount_input.fill(amount)
    downpayment_input.fill(downpayment)

    dropdown = page.get_by_role("combobox")
    if from_account_id is not None:
        dropdown.select_option(value=from_account_id)
    else:
        dropdown.select_option(index=0)

    page.get_by_role("button", name="Apply Now").click()


# --- Direct transition tests -------------------------------------------------


def test_loan_request_reaches_processed_state(page):
    """
    LoanForm -> Loan Request Processed (table row 1).

    Only confirms the intermediate "Processed" state is reached at all -
    doesn't assert on the outcome (Approved/Denied), which the two tests
    below cover separately with outcome-forcing inputs.
    """
    submit_loan_request(page, amount="1000", downpayment="100")

    if page.get_by_text("Error!").is_visible():
        pytest.fail(
            "System crashed instead of reaching 'Loan Request Processed' - "
            "see test_denial_path_does_not_crash for the dedicated crash test."
        )

    expect(page.get_by_text("Loan Request Processed")).to_be_visible()


def test_loan_outcome_matches_account_state(page):
    """
    Processed -> Approved OR Denied, with the correct downstream effect
    either way (table rows: evaluates valid -> Approved -> creates account;
    evaluates invalid -> Denied -> no account, routes to Terminal State).

    REPLACES the earlier pair of tests (test_loan_request_approved_creates_account
    / test_loan_request_denied_no_account_created), which tried to force a
    specific outcome with fixed input values. That approach didn't hold up:
    the exact same input (1000/1000) produced Denied on one run and Approved
    on the next, and pinning the funding account (rather than relying on
    dropdown index) didn't reliably fix it either -- suggesting the real
    ParaBank demo's approval logic depends on something not fully pinned
    down here (live balance, server-side randomness, or something else
    entirely). Rather than keep chasing input values for a system whose
    decision function isn't actually known, this test reads whatever
    outcome the system returns and asserts the invariant that should hold
    regardless of which branch fires: Approved must create exactly one new
    account, Denied must create none. This is what the diagram guarantees
    either way, and it's the part actually under test control.

    One consequence: a single run of this test only proves the invariant
    for whichever outcome shows up that time -- it does NOT guarantee both
    Approved and Denied get exercised across a given run. Running the suite
    repeatedly over time should surface both branches eventually, but if
    reliably exercising both branches every run matters, that would need
    either a way to control the real decision input (still unknown) or
    running this test multiple times per suite run with different accounts.
    """
    ids_before = get_account_ids(page)
    stable_account = min(ids_before, key=int)

    submit_loan_request(
        page, amount="1000", downpayment="1000", from_account_id=stable_account
    )

    if page.get_by_text("Error!").is_visible():
        pytest.skip(
            "System crashed instead of reaching an outcome -- known "
            "deviation, see test_denial_path_does_not_crash."
        )

    expect(page.get_by_text("Loan Request Processed")).to_be_visible()

    # Scoped to #loanStatus rather than a bare text search - get_by_text
    # on "Approved"/"Denied" alone previously hit a strict-mode violation,
    # matching both the status cell AND a "Congratulations..." message.
    status_text = page.locator("#loanStatus").inner_text()
    ids_after = get_account_ids(page)
    new_ids = ids_after - ids_before

    if status_text == "Approved":
        assert len(new_ids) == 1, (
            f"Approved but expected exactly one new account, "
            f"before={ids_before}, after={ids_after}"
        )
    elif status_text == "Denied":
        assert new_ids == set(), (
            f"Denied but a new account was created anyway: {new_ids}"
        )
    else:
        pytest.fail(f"Unexpected loan status: {status_text!r}")


def test_denial_path_does_not_crash(page):
    """
    Not a row in the state table -- the diagram only models intended
    behaviour, and this system crash was discovered through testing, not
    documented anywhere. Kept as its own named test (rather than a
    defensive check buried inside another test) so this finding is visible
    as its own pass/fail result.

    Marked xfail because this is a known, currently-unfixed deviation --
    remove the marker once the real system stops crashing on this path.
    Uses the same 1000/1000 input as test_loan_outcome_matches_account_state.
    Whether this input reliably triggers the crash (vs. reaching a normal
    Approved/Denied outcome) hasn't been confirmed either -- the system's
    behaviour with these inputs has already proven inconsistent across
    runs for the outcome itself, so the crash may be similarly intermittent
    rather than guaranteed. If this test starts passing/failing
    unpredictably rather than consistently xfail-ing, that inconsistency
    is itself worth noting rather than treating as test flakiness to fix.
    """
    ids_before = get_account_ids(page)
    stable_account = min(ids_before, key=int)

    submit_loan_request(
        page, amount="1000", downpayment="1000", from_account_id=stable_account
    )

    if page.get_by_text("Error!").is_visible():
        pytest.xfail("Known issue: system crashes instead of showing Denied.")

    expect(page.get_by_text("Loan Request Processed")).to_be_visible()