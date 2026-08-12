# Testing date validation for  https://open-meteo.com

# 1. End date cannot be before start date

# Equivalence Class Partitioning (ECP) - classes:
# End date before start date: invalid
# End date equal to start date: valid
# End date after start date: valid

# Boundary Value Analysis (BVA) - boundaries:
# 1. End date just before start date: invalid
# 2. End date equal to start date: valid
# 3. End date just after start date: valid

# 2. Start date and end date cannot be in the future

# Equivalence Class Partitioning (ECP) - classes:
# Start date in the future: invalid
# End date in the future: invalid
# Start date and end date in the past or present: valid

# Boundary Value Analysis (BVA) - boundaries:
# 1. Start date just before today: valid
# 2. Start date today: valid
# 3. Start date just after today: invalid

# 3. Sliding window for allowed date range

# Equivalence Class Partitioning (ECP) - classes:
# 1. Date before allowed window: invalid
# 2. Date at start of allowed window: valid
# 3. Date inside allowed window: valid
# 4. Date at end of allowed window: valid
# 5. Date after allowed window: invalid

# Boundary Value Analysis (BVA) - boundaries:
# 1. Just before start of allowed window: invalid
# 2. Start of allowed window: valid
# 3. Just after start of allowed window: valid
# 4. Just before end of allowed window: valid
# 5. End of allowed window: valid
# 6. Just after end of allowed window: invalid

# The window is dynamic and shifts based on the current date, so the boundaries will be calculated relative to current_date in the test code.
# The window spans from 3 months ago to 2 weeks from now, based on the API's response. 
# Therefore, the test code will need to calculate these dates dynamically to ensure they are always within the valid range when the tests are run.

import datetime
import pytest
import requests

current_date = datetime.date.today()

# Helper: fetch allowed date window dynamically
def get_allowed_window():
    url = "https://api.open-meteo.com/v1/forecast?latitude=0&longitude=0&hourly=temperature_2m"
    response = requests.get(url).json()
    # API returns allowed window in error messages, but also in metadata
    # Use metadata if available, fallback to parsing error message
    if "daily" in response:
        # Some endpoints include metadata, but forecast does not always
        pass
    # Fallback: intentionally trigger an out-of-range error to extract window
    bad_start = current_date + datetime.timedelta(days=400)
    bad_end = current_date + datetime.timedelta(days=401)
    error_resp = requests.get(
        f"https://api.open-meteo.com/v1/forecast?latitude=0&longitude=0&start_date={bad_start}&end_date={bad_end}&hourly=temperature_2m"
    ).json()
    reason = error_resp["reason"]
    # Extract dates from: "Parameter 'start_date' is out of allowed range from YYYY-MM-DD to YYYY-MM-DD"
    parts = reason.split("from ")[1].split(" to ")
    allowed_start = datetime.date.fromisoformat(parts[0])
    allowed_end = datetime.date.fromisoformat(parts[1])
    return allowed_start, allowed_end


# Helper: call API
def get_weather_data(start_date, end_date):
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude=0&longitude=0&start_date={start_date}&end_date={end_date}&hourly=temperature_2m"
    )
    return requests.get(url)


# 1. End date cannot be before start date

def test_end_date_before_start_date_different_days():
    start_date = current_date
    end_date = current_date - datetime.timedelta(days=1)
    response = get_weather_data(start_date, end_date)
    assert response.status_code == 400
    assert response.json()["error"] is True
    assert "End-date must be larger or equals than start-date" in response.json()["reason"]

def test_end_date_before_start_date_different_months():
    start_date = current_date
    end_date = current_date - datetime.timedelta(days=32)
    response = get_weather_data(start_date, end_date)
    assert response.status_code == 400
    assert response.json()["error"] is True
    assert "End-date must be larger or equals than start-date" in response.json()["reason"]

def test_end_date_before_start_date_different_years():
    start_date = current_date
    end_date = current_date - datetime.timedelta(days=365)
    response = get_weather_data(start_date, end_date)
    assert response.status_code == 400
    assert response.json()["error"] is True
    assert "End-date must be larger or equals than start-date" in response.json()["reason"]

def test_end_date_equal_to_start_date():
    start_date = current_date
    end_date = current_date
    response = get_weather_data(start_date, end_date)
    assert response.status_code == 200
    times = response.json()["hourly"]["time"]
    assert times[0].startswith(str(start_date))
    assert times[-1].startswith(str(end_date))

def test_end_date_after_start_date_same_month():
    start_date = current_date
    end_date = current_date + datetime.timedelta(days=1)
    response = get_weather_data(start_date, end_date)
    assert response.status_code == 200
    times = response.json()["hourly"]["time"]
    assert times[0].startswith(str(start_date))
    assert times[-1].startswith(str(end_date))

def test_end_date_after_start_date_different_months():
    start_date = current_date - datetime.timedelta(days=60)
    end_date = start_date + datetime.timedelta(days=1)
    response = get_weather_data(start_date, end_date)
    assert response.status_code == 200
    times = response.json()["hourly"]["time"]
    assert times[0].startswith(str(start_date))
    assert times[-1].startswith(str(end_date))


@pytest.mark.skip(reason="Year-boundary valid ranges cannot be tested unless current date is early in the year.")
def test_end_date_after_start_date_different_years():
    start_date = current_date + datetime.timedelta(days=365)
    end_date = start_date + datetime.timedelta(days=1)
    response = get_weather_data(start_date, end_date)
    assert response.status_code == 200


# 2. Start date and end date cannot be in the future

def test_start_date_in_future():
    start_date = current_date + datetime.timedelta(days=365)
    end_date = current_date
    response = get_weather_data(start_date, end_date)
    assert response.status_code == 400
    assert response.json()["error"] is True
    assert "End-date must be larger or equals than start-date" in response.json()["reason"]

def test_end_date_in_future():
    start_date = current_date - datetime.timedelta(days=1)
    end_date = current_date + datetime.timedelta(days=365)
    response = get_weather_data(start_date, end_date)
    assert response.status_code == 400
    assert response.json()["error"] is True
    assert "out of allowed range" in response.json()["reason"]

def test_start_date_and_end_date_in_past():
    start_date = current_date - datetime.timedelta(days=2)
    end_date = current_date - datetime.timedelta(days=1)
    response = get_weather_data(start_date, end_date)
    assert response.status_code == 200

def test_start_date_and_end_date_today():
    start_date = current_date
    end_date = current_date
    response = get_weather_data(start_date, end_date)
    assert response.status_code == 200


# 3. Sliding window for allowed date range

def test_date_before_allowed_window():
    allowed_start, _ = get_allowed_window()
    start_date = allowed_start - datetime.timedelta(days=1)
    end_date = allowed_start
    response = get_weather_data(start_date, end_date)
    assert response.status_code == 400
    assert "out of allowed range" in response.json()["reason"]

def test_date_at_start_of_allowed_window():
    allowed_start, _ = get_allowed_window()
    start_date = allowed_start
    end_date = allowed_start + datetime.timedelta(days=1)
    response = get_weather_data(start_date, end_date)
    assert response.status_code == 200

def test_date_inside_allowed_window():
    allowed_start, allowed_end = get_allowed_window()
    start_date = allowed_start + datetime.timedelta(days=10)
    end_date = allowed_start + datetime.timedelta(days=15)
    response = get_weather_data(start_date, end_date)
    assert response.status_code == 200

def test_date_at_end_of_allowed_window():
    _, allowed_end = get_allowed_window()
    start_date = allowed_end - datetime.timedelta(days=1)
    end_date = allowed_end
    response = get_weather_data(start_date, end_date)
    assert response.status_code == 200

def test_date_after_allowed_window():
    _, allowed_end = get_allowed_window()
    start_date = allowed_end + datetime.timedelta(days=1)
    end_date = allowed_end + datetime.timedelta(days=2)
    response = get_weather_data(start_date, end_date)
    assert response.status_code == 400
    assert "out of allowed range" in response.json()["reason"]
