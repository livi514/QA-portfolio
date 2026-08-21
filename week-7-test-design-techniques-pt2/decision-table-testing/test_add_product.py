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
    """
    Coarse helper: shifts the year but keeps today's month/day. Fine for
    cases like years_ago(50) where you just need "comfortably inside the
    valid range" -- but NOT precise enough for testing the exact 100-year
    boundary, since it always lands on a year-aligned date. See
    exact_100_year_boundary() below for day-precision boundary testing.
    """
    now = datetime.datetime.now()
    return now.replace(year=now.year - years)


def today() -> datetime.datetime:
    return datetime.datetime.now()


def exactly_100_years_ago() -> datetime.datetime:
    """
    Same as years_ago(100), but named explicitly since it's used as the
    zero-point for day-precision boundary math below.
    """
    now = datetime.datetime.now()
    return now.replace(year=now.year - 100)


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
    errors = submit(
        page, name="Valid Product", price="10.00", date=exactly_100_years_ago()
    )
    print(f"\nExactly-100-years-ago errors: {errors}")


# --- Day-precision boundary tests -----------------------------------------
#
# years_ago(n) uses datetime.replace(year=...), which only ever moves the
# year and keeps today's month/day fixed. That means years_ago(100) and
# years_ago(101) both land exactly on a year anniversary of today -- neither
# one can tell you whether the real system checks the boundary at day-level
# precision or just compares year numbers.
#
# Concretely: if today is 21/08/2026, years_ago(100) is 21/08/1926 and
# years_ago(101) is 21/08/1925. But 20/08/1926 -- one day older than the
# true 100-year boundary -- is *also* over 100 years ago (100 years and
# 1 day), and a naive year-only check (e.g. today.year - date.year > 100)
# would wrongly treat it as exactly 100, not over. Neither existing test
# would ever catch that, since neither ever produces a date one day off
# the true boundary.
#
# These two tests isolate that specifically, using real date arithmetic
# (timedelta on the exact-100-years date) rather than the coarser
# year-jump helper, so a day-precision bug like the one above would
# actually fail one of these.


def test_just_over_100_years_ago_date(page):
    """
    Date is 100 years and 1 day ago -> should be Invalid.

    This is the case a year-only comparison would get wrong: naive logic
    comparing just today.year - date.year would see exactly 100 and treat
    it as the (valid) boundary, missing that it's actually 1 day past it.
    """
    date = exactly_100_years_ago() - datetime.timedelta(days=1)
    errors = submit(page, name="Valid Product", price="10.00", date=date)
    assert any("100 years" in e or "old" in e.lower() for e in errors), f"Got: {errors}"


def test_just_under_100_years_ago_date(page):
    """
    Date is 1 day short of 100 years ago (99 years, 364/365 days) -> should
    be Valid. Companion to test_just_over_100_years_ago_date -- confirms
    the boundary doesn't reject dates that are genuinely still within range.
    """
    date = exactly_100_years_ago() + datetime.timedelta(days=1)
    errors = submit(page, name="Valid Product", price="10.00", date=date)
    assert not any(
        "100 years" in e or "old" in e.lower() for e in errors
    ), f"Got: {errors}"


def test_valid_past_100_years_date(page):
    """
    R7: Date within past 100 years → Valid.

    Confirmed real success behaviour: the form redirects to the product
    list page, where the newly added product appears. Uses a unique,
    timestamped product name rather than the generic "Valid Product" used
    elsewhere in this file, since the site persists submissions -- a fixed
    name would make it ambiguous whether a given list entry came from this
    test run or a previous one.
    """
    unique_name = f"Valid Product {datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
    errors = submit(page, name=unique_name, price="10.00", date=years_ago(50))
    assert errors == [], f"Expected no validation errors, got: {errors}"

    # submit()'s internal 500ms wait covers inline validation rendering, but
    # may not be enough for a full page redirect to complete -- wait
    # explicitly here before checking URL/list state.
    page.wait_for_load_state("networkidle")

    # Confirm the redirect away from the add-product form.
    assert "/add-product" not in page.url, f"Expected redirect, still on: {page.url}"

    # Confirm the new product is actually visible in the resulting list --
    # this is the real proof of success, not just the absence of errors.
    assert page.get_by_text(unique_name).is_visible(), (
        f"Expected '{unique_name}' to appear in the product list after submission, "
        f"but it wasn't found on {page.url}"
    )
