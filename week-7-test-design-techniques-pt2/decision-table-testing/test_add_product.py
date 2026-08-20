# See decision-table-for-commitquality.md for the decision table that these tests are based on.

# 1. Each collapsed rule becomes one test case.
# We now have 7 rules, so 7 test cases.
# R1 -> test invalid name
# R2 -> test empty price
# R3 -> test >10 digit price
# R4 -> test empty date
# R5 -> test future/today date
# R6 -> test over-100-years-ago date
# R7 -> test valid past-100-years date

# 2. Convert abstract conditions into concrete test data.

# R1 -> test invalid name
# name = ""

# R2 -> test empty price
# price = ""

# R3 -> test >10 digit price
# price = "12345678901"

# R4 -> test empty date
# date = ""

# R5 -> test future/today date
# date = datetime.now()

# R6 -> test over-100-years-ago date
# date = datetime.now().replace(year=datetime.now().year - 101)

# R7 -> test valid past-100-years date
# date = datetime.now().replace(year=datetime.now().year - 50)

# 3. Write Python tests using those values.

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

# Playwright submit() helper

def submit(name, price, date):
    """
    Interacts with the real CommitQuality website and returns the validation message.
    """

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(URL)

        # Fill name and price
        page.fill("#name", str(name))
        page.fill("#price", str(price))

        # Correct HTML date input format: YYYY-MM-DD
        if date == "" or date is None:
            page.fill("#dateStocked", "")
        else:
            page.fill("#dateStocked", date.strftime("%Y-%m-%d"))

        # Submit form
        page.click("button[type='submit']")

        # Try to wait for an error message
        try:
            page.wait_for_selector(".error-message", timeout=3000)
            message = page.inner_text(".error-message")
        except:
            # No error message → valid input
            message = ""

        browser.close()
        return message


# Rule-based test cases

def test_invalid_name():
    """R1: Name < 2 characters → Invalid"""
    result = submit(
        name="",
        price="10.00",
        date=years_ago(50)
    )
    assert result == "Name must be at least 2 characters."


def test_empty_price():
    """R2: Price empty → Invalid"""
    result = submit(
        name="Valid Product",
        price="",
        date=years_ago(50)
    )
    assert result == "Price must not be empty and within 10 digits"


def test_price_too_long():
    """R3: Price > 10 digits → Invalid"""
    result = submit(
        name="Valid Product",
        price="12345678901",  # 11 digits
        date=years_ago(50)
    )
    assert result == "Price must not be empty and within 10 digits"


def test_empty_date():
    """R4: Date empty → Invalid"""
    result = submit(
        name="Valid Product",
        price="10.00",
        date=""
    )
    assert result == "Date must not be empty."

# Broke this down into two tests: today and future, in case system behaviour changes.

def test_today_date():
    """R5a: Date is today → Invalid (confirmed via testing, not documented)"""
    result = submit(name="Valid Product", price="10.00", date=today())
    assert result == "Date must not be in the future."

def test_future_date():
    """R5b: Date is clearly in the future → Invalid"""
    result = submit(name="Valid Product", price="10.00", date=today() + datetime.timedelta(days=30))
    assert result == "Date must not be in the future."

# Boundary test
def test_exactly_100_years_ago():
    """Boundary: exactly 100 years ago — table doesn't specify inclusive/exclusive"""
    result = submit(name="Valid Product", price="10.00", date=years_ago(100))
    # Run this and see what the real system does, then assert accordingly —
    # this determines whether your table's "Past 100 years" class boundary is correct

def test_over_100_years_ago_date():
    """R6: Date older than 100 years → Invalid"""
    result = submit(
        name="Valid Product",
        price="10.00",
        date=years_ago(101)
    )
    assert result == "Date must not be older than 100 years."


def test_valid_past_100_years_date():
    """R7: Date within past 100 years → Valid"""
    result = submit(
        name="Valid Product",
        price="10.00",
        date=years_ago(50)
    )
    assert result == ""
