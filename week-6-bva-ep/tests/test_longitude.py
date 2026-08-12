import pytest
import requests

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

def get_weather_data(longitude):
    url = f"https://api.open-meteo.com/v1/forecast?latitude=0&longitude={longitude}&hourly=temperature_2m"
    return requests.get(url)

@pytest.mark.parametrize("longitude", [
    -180.0, -179.9, -90.0, 0.0, 90.0, 179.9, 180.0
])
def test_valid_longitude(longitude):
    response = get_weather_data(longitude)
    assert response.status_code == 200
    assert "longitude" in response.json()

    # Special case: API normalises 180 → -180
    if longitude == 180.0:
        assert response.json()["longitude"] == pytest.approx(-180.0, abs=0.1)
    else:
        assert response.json()["longitude"] == pytest.approx(longitude, abs=0.1)

@pytest.mark.parametrize("longitude", [
    -180.0001, -181.0, -200.0,
    180.0001, 181.0, 200.0
])
def test_invalid_longitude(longitude):
    response = get_weather_data(longitude)

    # API may return 400 or 503 depending on internal routing
    assert response.status_code in (400, 503)

    # Error field may not exist on 503 responses
    reason = response.json().get("reason", "")
    assert "Longitude must be in range" in reason
