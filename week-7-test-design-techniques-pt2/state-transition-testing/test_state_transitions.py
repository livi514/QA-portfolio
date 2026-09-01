# See state-transition-table.md for the full state transition table these
# tests are based on. Only rows marked "Direct" in that table are exercised
# here. "Structural" rows (for example, the absence of a deny-after-approve
# transition or the duplicate-submission case after real UI review) are not
# tested because there is no UI action that could trigger them.

import pytest
from playwright.sync_api import expect, sync_playwright

LOGIN_URL = "https://parabank.parasoft.com/parabank/index.htm"


# --- Fixtures ---------------------------------------------------------------


@pytest.fixture
def page():
    """
    Function-scoped rather than module-scoped, because loan requests mutate
    account state. Each test should start from a fresh login instead of
    sharing state or history with another test in the file. This means more
    browser launches, but it avoids one test's submitted loan bleeding into
    another test's assertion about whether a new loan account exists.
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
    Return the set of account IDs currently listed in Accounts Overview.

    Added after review: there is no "Loan Account" label anywhere on the real
    Accounts Overview page. This was confirmed via a real test run, where
    accounts are listed only by numeric ID in a shared table alongside every
    other account type (checking, savings, and loan all look identical).
    Therefore, determining whether a loan account was created can only be done
    structurally by comparing the account list before and after submission,
    rather than searching for text that does not exist on the page.
    """
    page.click("a[href*='overview']")
    expect(page.get_by_role("heading", name="Accounts Overview")).to_be_visible()

    # Wait for the AJAX-populated table body to actually contain rows rather
    # than reading it immediately, because the table can initially be empty
    # when the page first renders.
    page.wait_for_selector("#accountTable tbody tr", timeout=10000)

    # Account IDs appear as link text in the first column of the table, for
    # example "13344" or "16341", linking to activity.htm?id=<id>.
    id_links = page.locator("#accountTable a[href*='activity.htm?id=']")
    return {id_links.nth(i).inner_text() for i in range(id_links.count())}


def submit_loan_request(
    page, amount: str, downpayment: str, from_account_id: str = None
):
    """
    Navigate to the loan form, fill it in, and submit it.

    Returns the page in whatever state it lands on thereafter (Processed,
    an outcome screen, or an Error page). The caller is responsible for
    asserting which outcome is expected next.
    """
    page.click('a[href*="requestloan"]')
    expect(page.get_by_role("heading", name="Apply for a Loan")).to_be_visible()

    # ParaBank has no labels or IDs on the amount and downpayment fields, so
    # we select by index. This is order-dependent and would silently break if
    # ParaBank reorders the form.
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
    Loan Form -> Loan Request Processed (table row 1).

    This confirms only that the intermediate "Processed" state is reached.
    It does not assert on the outcome (Approved/Denied), which is covered by
    the tests below.
    """
    submit_loan_request(page, amount="1000", downpayment="100")

    if page.get_by_text("Error!").is_visible():
        pytest.fail(
            "System crashed instead of reaching 'Loan Request Processed'. "
            "See test_denial_path_does_not_crash for the dedicated crash test."
        )

    expect(page.get_by_text("Loan Request Processed")).to_be_visible()


def test_loan_outcome_matches_account_state(page):
    """
    Processed -> Approved OR Denied, with the correct downstream effect in
    either case.

    This replaces the earlier pair of tests that attempted to force a specific
    outcome with fixed input values. That approach did not hold up: the exact
    same input (1000/1000) produced Denied on one run and Approved on the
    next, and pinning the funding account did not reliably fix it either.
    This suggests the real ParaBank approval logic depends on something not
    fully understood here, such as live balance data, server-side logic, or
    another input not controlled in this test.

    Rather than keep chasing the exact inputs for a system whose decision
    function is not fully known, this test reads whatever outcome the system
    returns and asserts the invariant that should hold regardless of which
    branch fires: Approved must create exactly one new account, and Denied
    must create none. This is the behaviour guaranteed by the diagram and the
    underlying state model.

    One consequence is that a single run of this test proves the invariant for
    whichever outcome appears that time only. It does not guarantee that both
    Approved and Denied are exercised in a single run. Re-running the suite
    over time should surface both branches eventually, but if reliably
    exercising both outcomes in one run matters, that would require either a
    way to control the decision input or multiple runs with different inputs.
    """
    ids_before = get_account_ids(page)
    stable_account = min(ids_before, key=int)

    submit_loan_request(
        page, amount="1000", downpayment="1000", from_account_id=stable_account
    )

    if page.get_by_text("Error!").is_visible():
        pytest.skip(
            "System crashed instead of reaching an outcome; see "
            "test_denial_path_does_not_crash for the known deviation."
        )

    expect(page.get_by_text("Loan Request Processed")).to_be_visible()

    # Scope to #loanStatus rather than using a bare text search. A plain
    # get_by_text("Approved"/"Denied") previously hit a strict-mode violation,
    # matching both the status cell and a success message.
    status_text = page.locator("#loanStatus").inner_text()
    ids_after = get_account_ids(page)
    new_ids = ids_after - ids_before

    if status_text == "Approved":
        assert len(new_ids) == 1, (
            f"Approved but expected exactly one new account; "
            f"before={ids_before}, after={ids_after}"
        )
    elif status_text == "Denied":
        assert (
            new_ids == set()
        ), f"Denied but a new account was created anyway: {new_ids}"
    else:
        pytest.fail(f"Unexpected loan status: {status_text!r}")


def test_denial_path_does_not_crash(page):
    """
    This is not a row in the state table. The diagram models intended
    behaviour only, and this system crash was discovered during testing rather
    than documented in advance.

    We keep it as its own named test so the finding is visible as an explicit
    result rather than being buried inside a different test's assertion.

    Marked xfail because this is a known, currently unfixed deviation. Remove
    the marker once the real system stops crashing on this path.

    It uses the same 1000/1000 input as test_loan_outcome_matches_account_state.
    Whether this input reliably triggers the crash or reaches a normal
    Approved/Denied outcome has not been confirmed. The system's behaviour with
    the same inputs has already proved inconsistent across runs, so the crash
    may be similarly intermittent rather than guaranteed. If this test begins
    passing or failing unpredictably rather than consistently xfail-ing, that
    inconsistency is itself worth noting rather than treating as test flakiness.
    """
    ids_before = get_account_ids(page)
    stable_account = min(ids_before, key=int)

    submit_loan_request(
        page, amount="1000", downpayment="1000", from_account_id=stable_account
    )

    if page.get_by_text("Error!").is_visible():
        pytest.xfail("Known issue: system crashes instead of showing Denied.")

    expect(page.get_by_text("Loan Request Processed")).to_be_visible()
