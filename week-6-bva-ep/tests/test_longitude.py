import pytest
from conftest import get_weather_data

# Longitude tests for https://open-meteo.com
#
# Equivalence Class Partitioning (ECP):
# - Valid:   -180 ≤ longitude ≤ 180
# - Invalid: longitude < -180 or longitude > 180
#
# Boundary Value Analysis (BVA):
# -180 (lower boundary)
# -179.9 (just above)
# -180.0001 (just below)
# 180 (upper boundary)
# 179.9 (just below)
# 180.0001 (just above)


# get_weather_data now comes from conftest.py, shared with test_dates.py and
# test_latitude.py. longitude is passed by keyword; latitude stays at the
# conftest default (0).


@pytest.mark.parametrize("longitude", [-180.0, -179.9, -90.0, 0.0, 90.0, 179.9, 180.0])
def test_valid_longitude(longitude):
    response = get_weather_data(longitude=longitude)
    assert response.status_code == 200
    assert "longitude" in response.json()

    # Special case: API normalises 180 → -180
    if longitude == 180.0:
        assert response.json()["longitude"] == pytest.approx(-180.0, abs=0.1)
    else:
        assert response.json()["longitude"] == pytest.approx(longitude, abs=0.1)


@pytest.mark.parametrize(
    "longitude", [-180.0001, -181.0, -200.0, 180.0001, 181.0, 200.0]
)
def test_invalid_longitude(longitude):
    response = get_weather_data(longitude=longitude)

    # API may return 400 or 503 depending on internal routing
    assert response.status_code in (400, 503)

    # Error field may not exist on 503 responses
    reason = response.json().get("reason", "")
    assert "Longitude must be in range" in reason
