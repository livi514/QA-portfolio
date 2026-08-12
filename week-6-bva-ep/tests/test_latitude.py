import pytest
import requests

# Latitude tests for https://open-meteo.com
#
# Equivalence Class Partitioning (ECP):
# - Valid:   -90 ≤ latitude ≤ 90
# - Invalid: latitude < -90 or latitude > 90
#
# Boundary Value Analysis (BVA):
# -90 (lower boundary)
# -89.9 (just above)
# -90.0001 (just below)
# 90 (upper boundary)
# 89.9 (just below)
# 90.0001 (just above)

def get_weather_data(latitude):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude=0&hourly=temperature_2m"
    return requests.get(url)


# Valid latitude values (ECP + BVA)
@pytest.mark.parametrize("latitude", [
    -90.0, -89.9, -45.0, 0.0, 45.0, 89.9, 90.0
])
def test_valid_latitude(latitude):
    response = get_weather_data(latitude)
    assert response.status_code == 200
    assert "latitude" in response.json()
    # API returns floats with slight rounding differences
    assert response.json()["latitude"] == pytest.approx(latitude, abs=0.1)


# Invalid latitude values (ECP + BVA)
@pytest.mark.parametrize("latitude", [
    -90.0001, -91.0, -100.0,
    90.0001, 91.0, 100.0
])
def test_invalid_latitude(latitude):
    response = get_weather_data(latitude)
    assert response.status_code == 400
    assert response.json()["error"] is True
    assert "Latitude must be in range" in response.json()["reason"]
