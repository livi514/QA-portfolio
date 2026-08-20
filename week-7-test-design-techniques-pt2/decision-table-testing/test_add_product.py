# See decision-table-for-commitquality.md for the decision table that these tests are based on.

# --- What changed and why -------------------------------------------------
#
# The original submit() assumed a single #message element holding the
# validation text. The diagnostic script (diagnose_commitquality.py) proved
# that selector doesn't exist anywhere on the page -- which is why every
# single test timed out identically, including the valid-data case.
#
# The real structure, confirmed from one diagnostic run (empty name, valid
# price, valid date):
#   - Each invalid field gets its own inline <div class="error-message">
#     next to that field's input. This div has NO data-testid of its own.
#   - There's also a page-level <div class="error-message"
#     data-testid="fillin-all-fields-validation">Please fill in all
#     fields</div>
#   - And a page-level <div class="error" data-testid="all-fields-validation">
#     Errors must be resolved before submitting</div>
#   - The form has novalidate="" -- no native HTML5 blocking, confirmed.
#
# IMPORTANT: the diagnostic only exercised ONE rule (invalid name, valid
# price, valid date). The selectors/behaviour for the other 6 rules --
# price too long, empty price, empty date, today, future, over-100-years --
# have NOT been confirmed against the live DOM. Rather than guess new
# selectors per rule (the same mistake that caused the original failure),
# submit() below collects ALL visible error text on the page generically,
# and each test asserts its expected message is present in that collection.
# This should work regardless of which specific div structure each rule
# uses, but the exact expected message text below is still only confirmed
# for R1 (invalid name) -- the rest need a real run to verify, flagged
# individually below.

import datetime

import pytest
from playwright.sync_api import sync_playwright

URL = "https://commitquality.com/add-product"


# Utility functions


def years_ago(years: int) -> datetime.datetime:
    now = datetime.datetime.now()
    return now.replace(year=now.year - years)


def today() -> datetime.datetime:
    return datetime.datetime.now()


# Browser fixture


@pytest.fixture(scope="module")
def page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        pg = browser.new_page()
        yield pg
        browser.close()


def submit(page, name, price, date):
    """
    Interacts with the real CommitQuality website and returns all visible
    validation error text on the page as a list of strings.

    Returns a list rather than one message because the real page can show
    multiple errors at once (a per-field inline error plus the page-level
    "Please fill in all fields" / "Errors must be resolved before
    submitting" messages) -- there's no single element that captures
    "the" validation outcome the way the original #message assumption did.

    On a fully valid submission, this should return an empty list -- but
    that's unconfirmed; see test_valid_past_100_years_date for the TODO
    to verify what real success actually looks like (redirect, confirmation
    message, product appearing elsewhere, etc.), since an empty error list
    only proves nothing failed, not that anything succeeded.
    """
    page.goto(URL, wait_until="networkidle")

    page.fill("#name", str(name))
    page.fill("#price", str(price))

    if date == "" or date is None:
        page.fill("#dateStocked", "")
    else:
        page.fill("#dateStocked", date.strftime("%Y-%m-%d"))

    page.click("button[type='submit']")

    # Give the SPA a moment to render any validation state after click,
    # rather than waiting on one specific selector that may not apply
    # to every rule.
    page.wait_for_timeout(500)

    # Collect every visible error element on the page: both the per-field
    # inline errors (class="error-message", no data-testid) and the two
    # known page-level ones (data-testid="fillin-all-fields-validation"
    # and data-testid="all-fields-validation").
    error_texts = page.locator(".error-message, .error").all_inner_texts()

    # Filter out empty strings (locator can pick up elements present in the
    # DOM but not populated/visible depending on render timing).
    return [text.strip() for text in error_texts if text.strip()]


# Rule-based test cases


def test_invalid_name(page):
    """
    R1: Name < 2 characters → Invalid.

    Confirmed against the live DOM via diagnose_commitquality.py --
    message text includes the trailing period, which the original test
    was missing ("...characters" vs "...characters.").
    """
    errors = submit(page, name="", price="10.00", date=years_ago(50))
    assert "Name must be at least 2 characters." in errors, f"Got: {errors}"


def test_empty_price(page):
    """
    R2: Price empty → Invalid.

    NOT YET CONFIRMED against the live DOM -- the diagnostic run only
    exercised an invalid name with a valid price. Run this and check the
    real error text before trusting this assertion; update it to match.
    """
    errors = submit(page, name="Valid Product", price="", date=years_ago(50))
    # TODO: confirm real message text -- placeholder based on the original
    # (unverified) assumption.
    assert any("price" in e.lower() for e in errors), f"Got: {errors}"


def test_price_too_long(page):
    """
    R3: Price > 10 digits → Invalid.

    NOT YET CONFIRMED -- see test_empty_price note above.
    """
    errors = submit(
        page, name="Valid Product", price="12345678901", date=years_ago(50)  # 11 digits
    )
    assert any("price" in e.lower() for e in errors), f"Got: {errors}"


def test_price_at_10_digit_boundary(page):
    """
    Boundary (not in the collapsed table): confirms the table's <=10-digit
    Valid class actually holds at exactly 10 digits.

    NOT YET CONFIRMED what a fully valid submission looks like -- see
    test_valid_past_100_years_date TODO. This currently just asserts no
    price-related error appears.
    """
    errors = submit(
        page, name="Valid Product", price="1234567890", date=years_ago(50)  # 10 digits
    )
    assert not any("price" in e.lower() for e in errors), f"Got: {errors}"


def test_empty_date(page):
    """
    R4: Date empty → Invalid.

    NOT YET CONFIRMED -- see test_empty_price note above.
    """
    errors = submit(page, name="Valid Product", price="10.00", date="")
    assert any("date" in e.lower() for e in errors), f"Got: {errors}"


def test_today_date(page):
    """
    R5a: Date is today → Invalid.

    NOT YET CONFIRMED -- see test_empty_price note above. Kept as its own
    test (rather than folded into test_future_date) because the original
    suite's comment flagged today's date as producing non-obvious system
    behaviour worth locking down individually.
    """
    errors = submit(page, name="Valid Product", price="10.00", date=today())
    assert any("future" in e.lower() for e in errors), f"Got: {errors}"


def test_future_date(page):
    """
    R5b: Date is clearly in the future (not just today) → Invalid.

    NOT YET CONFIRMED -- see test_empty_price note above.
    """
    errors = submit(
        page,
        name="Valid Product",
        price="10.00",
        date=today() + datetime.timedelta(days=30),
    )
    assert any("future" in e.lower() for e in errors), f"Got: {errors}"


def test_over_100_years_ago_date(page):
    """
    R6: Date older than 100 years → Invalid.

    NOT YET CONFIRMED -- see test_empty_price note above.
    """
    errors = submit(page, name="Valid Product", price="10.00", date=years_ago(101))
    assert any("100 years" in e or "old" in e.lower() for e in errors), f"Got: {errors}"


def test_exactly_100_years_ago_date(page):
    """
    Boundary (not in the collapsed table): whether exactly 100 years ago is
    Valid or Invalid per the real system -- the table doesn't specify
    inclusive/exclusive.

    NOT YET CONFIRMED. Deliberately unopinionated -- no assertion on outcome
    yet, just observes. Run with -s to see the printed result, then decide
    the assertion and update the decision table doc to state the boundary
    explicitly either way.
    """
    errors = submit(page, name="Valid Product", price="10.00", date=years_ago(100))
    print(f"\nExactly-100-years-ago errors: {errors}")


def test_valid_past_100_years_date(page):
    """
    R7: Date within past 100 years → Valid.

    NOT YET CONFIRMED what real success looks like. This only proves no
    error text appeared -- it does NOT yet prove the product was actually
    added (could be a silent no-op, a redirect not being followed, etc.).
    Once you've checked the live site's real success behaviour (redirect?
    confirmation message? product visible on /products?), extend this with
    a positive assertion rather than relying solely on an empty error list.
    """
    errors = submit(page, name="Valid Product", price="10.00", date=years_ago(50))
    assert errors == [], f"Expected no validation errors, got: {errors}"
    # TODO: add positive confirmation of success once real behaviour is known.
