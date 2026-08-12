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


# Valid longitude values (ECP + BVA)
@pytest.mark.parametrize("longitude", [
    -180.0, -179.9, -90.0, 0.0, 90.0, 179.9, 180.0
])
def test_valid_longitude(longitude):
    response = get_weather_data(longitude)
    assert response.status_code == 200
    assert "longitude" in response.json()
    # API returns floats with slight rounding differences
    assert response.json()["longitude"] == pytest.approx(longitude, abs=0.1)


# Invalid longitude values (ECP + BVA)
@pytest.mark.parametrize("longitude", [
    -180.0001, -181.0, -200.0,
    180.0001, 181.0, 200.0
])
def test_invalid_longitude(longitude):
    response = get_weather_data(longitude)
    assert response.status_code == 400
    assert response.json()["error"] is True
    assert "Longitude must be in range" in response.json()["reason"]
