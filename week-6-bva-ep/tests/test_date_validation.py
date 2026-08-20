import datetime

import pytest
from conftest import get_weather_data

current_date = datetime.date.today()

# Testing date validation for https://open-meteo.com
#
# This suite applies Equivalence Class Partitioning (ECP) and Boundary Value Analysis (BVA)
# to the API's date-handling rules. The API enforces three major constraints:
#
# 1. End date cannot be before start date
#
#    ECP classes:
#      - Invalid: end date < start date
#      - Valid:   end date = start date
#      - Valid:   end date > start date
#
#    BVA boundaries:
#      - End date just before start date → invalid
#      - End date equal to start date → valid
#      - End date just after start date → valid
#
#
# 2. Start date and end date cannot be in the future
#
#    ECP classes:
#      - Invalid: start date in the future
#      - Invalid: end date in the future
#      - Valid:   both dates in the past or present
#
#    BVA boundaries:
#      - Start date just before today → valid
#      - Start date equal to today → valid
#      - Start date just after today → invalid
#
#    NOTE: to isolate this rule from the end-before-start rule (constraint 1),
#    the future-date tests below keep start_date < end_date and both in the
#    future, so ordering is always satisfied and any failure is attributable
#    to the future-date check specifically (or to the sliding window, if the
#    API turns out not to have a distinct future-date rule at all -- see the
#    reason string assertions, which are left loose deliberately so a real
#    run reveals which message actually fires).
#
#
# 3. Sliding window for allowed date range
#
#    The API only allows requests within a dynamic window that shifts daily.
#    The window typically spans ~3 months into the past and ~2 weeks into the future.
#    Because this range changes every day, the tests compute the boundaries dynamically.
#
#    ECP classes:
#      - Invalid: date before allowed window
#      - Valid:   date at start of allowed window
#      - Valid:   date inside allowed window (interior, not a boundary)
#      - Valid:   date at end of allowed window
#      - Invalid: date after allowed window
#
#    BVA boundaries (all six from Robust BVA, tested individually below):
#      - Just before allowed window start → invalid
#      - Allowed window start → valid
#      - Just after allowed window start → valid
#      - Just before allowed window end → valid
#      - Allowed window end → valid
#      - Just after allowed window end → invalid
#
#    Because the window is dynamic, all boundary dates are calculated relative to
#    the current date and the API's reported allowed range.


# --- Helpers -------------------------------------------------------------
#
# get_weather_data now comes from conftest.py (shared across test_dates.py,
# test_latitude.py, test_longitude.py). It takes latitude/longitude/start_date/
# end_date as optional kwargs -- this file only ever passes start_date/end_date,
# leaving latitude/longitude at their conftest defaults (0, 0).


def extract_allowed_window():
    """
    The API's allowed date window shifts daily.
    We intentionally trigger an out-of-range error and parse the window.
    """
    bad_start = current_date + datetime.timedelta(days=400)
    bad_end = current_date + datetime.timedelta(days=401)

    resp = get_weather_data(start_date=bad_start, end_date=bad_end).json()

    # Guard against the API returning a response with no "reason" key (already
    # observed as a possibility for invalid longitude -- 503 with no error body).
    # Without this, a shape change here fails as a confusing KeyError instead of
    # a readable assertion, and takes every sliding-window test down with it
    # since this fixture is module-scoped.
    assert "reason" in resp, (
        f"Expected 'reason' in response when triggering an out-of-range date, "
        f"got: {resp}"
    )
    reason = resp["reason"]
    window = reason.split("from ")[1]
    start_str, end_str = window.split(" to ")
    allowed_start = datetime.date.fromisoformat(start_str)
    allowed_end = datetime.date.fromisoformat(end_str)
    return allowed_start, allowed_end


@pytest.fixture(scope="module")
def allowed_window():
    return extract_allowed_window()


# --- 1. End date cannot be before start date -----------------------------


@pytest.mark.parametrize("delta", [1, 32, 365])
def test_end_date_before_start_date(delta):
    start_date = current_date
    end_date = current_date - datetime.timedelta(days=delta)
    response = get_weather_data(start_date=start_date, end_date=end_date)
    assert response.status_code == 400
    assert response.json()["error"] is True
    assert (
        "End-date must be larger or equals than start-date" in response.json()["reason"]
    )


def test_end_date_equal_to_start_date():
    start_date = current_date
    end_date = current_date
    response = get_weather_data(start_date=start_date, end_date=end_date)
    assert response.status_code == 200
    times = response.json()["hourly"]["time"]
    assert times[0].startswith(str(start_date))
    assert times[-1].startswith(str(end_date))


@pytest.mark.parametrize("delta", [1, 30, 60])
def test_end_date_after_start_date(delta):
    start_date = current_date - datetime.timedelta(days=delta)
    end_date = start_date + datetime.timedelta(days=1)
    response = get_weather_data(start_date=start_date, end_date=end_date)
    assert response.status_code == 200


# --- 2. Future dates -------------------------------------------------------


def test_start_date_in_future():
    start_date = current_date + datetime.timedelta(days=365)
    end_date = start_date + datetime.timedelta(days=1)
    response = get_weather_data(start_date=start_date, end_date=end_date)
    assert response.status_code == 400
    # Run this once manually and confirm which message actually comes back --
    # the API may not have a distinct "future date" rule separate from the
    # sliding window's "out of allowed range" message. Whichever it is,
    # update this assertion to match and note the finding in the writeup.
    assert "out of allowed range" in response.json()["reason"]


def test_end_date_in_future():
    start_date = current_date - datetime.timedelta(days=1)
    end_date = current_date + datetime.timedelta(days=365)
    response = get_weather_data(start_date=start_date, end_date=end_date)
    assert response.status_code == 400
    assert "out of allowed range" in response.json()["reason"]


def test_start_and_end_in_past():
    start_date = current_date - datetime.timedelta(days=2)
    end_date = current_date - datetime.timedelta(days=1)
    response = get_weather_data(start_date=start_date, end_date=end_date)
    assert response.status_code == 200


def test_start_and_end_today():
    start_date = current_date
    end_date = current_date
    response = get_weather_data(start_date=start_date, end_date=end_date)
    assert response.status_code == 200


# --- 3. Sliding window ----------------------------------------------------


def test_date_before_allowed_window(allowed_window):
    allowed_start, _ = allowed_window
    start_date = allowed_start - datetime.timedelta(days=1)
    end_date = allowed_start
    response = get_weather_data(start_date=start_date, end_date=end_date)
    assert response.status_code == 400
    assert "out of allowed range" in response.json()["reason"]


def test_date_at_start_of_allowed_window(allowed_window):
    allowed_start, _ = allowed_window
    start_date = allowed_start
    end_date = allowed_start + datetime.timedelta(days=1)
    response = get_weather_data(start_date=start_date, end_date=end_date)
    assert response.status_code == 200


def test_date_just_after_start_of_allowed_window(allowed_window):
    allowed_start, _ = allowed_window
    start_date = allowed_start + datetime.timedelta(days=1)
    end_date = start_date + datetime.timedelta(days=1)
    response = get_weather_data(start_date=start_date, end_date=end_date)
    assert response.status_code == 200


def test_date_inside_allowed_window_interior(allowed_window):
    """Valid-interior case (ECP), not a boundary -- kept separate from BVA proper."""
    allowed_start, allowed_end = allowed_window
    start_date = allowed_start + datetime.timedelta(days=10)
    end_date = allowed_start + datetime.timedelta(days=15)
    response = get_weather_data(start_date=start_date, end_date=end_date)
    assert response.status_code == 200


def test_date_just_before_end_of_allowed_window(allowed_window):
    _, allowed_end = allowed_window
    end_date = allowed_end - datetime.timedelta(days=1)
    start_date = end_date - datetime.timedelta(days=1)
    response = get_weather_data(start_date=start_date, end_date=end_date)
    assert response.status_code == 200


def test_date_at_end_of_allowed_window(allowed_window):
    _, allowed_end = allowed_window
    start_date = allowed_end - datetime.timedelta(days=1)
    end_date = allowed_end
    response = get_weather_data(start_date=start_date, end_date=end_date)
    assert response.status_code == 200


def test_date_after_allowed_window(allowed_window):
    _, allowed_end = allowed_window
    start_date = allowed_end + datetime.timedelta(days=1)
    end_date = allowed_end + datetime.timedelta(days=2)
    response = get_weather_data(start_date=start_date, end_date=end_date)
    assert response.status_code == 400
    assert "out of allowed range" in response.json()["reason"]


def test_both_dates_outside_window(allowed_window):
    allowed_start, allowed_end = allowed_window
    start_date = allowed_start - datetime.timedelta(days=5)
    end_date = allowed_end + datetime.timedelta(days=5)
    response = get_weather_data(start_date=start_date, end_date=end_date)
    assert response.status_code == 400
    assert "out of allowed range" in response.json()["reason"]
