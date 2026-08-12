import requests
import pytest

# Longitude tests for https://open-meteo.com

# Equivalence Class Partitioning (ECP) - classes:
# 1. Valid longitude values: -180 to 180
# 2. Invalid longitude values: less than -180 or greater than 180

# Boundary Value Analysis (BVA) - boundaries:
# 1. Lower boundary: -180
# 2. Upper boundary: 180
# 3. Just below lower boundary: -180.1
# 4. Just above upper boundary: 180.1

#  Test cases for valid longitude values
@pytest.mark.parametrize("longitude", [-180.0, -179.9, -179.0, 0.0, 90.0, 179.0, 179.9, 180.0])
def test_valid_longitude(longitude):
    response = get_weather_data(longitude)
    assert response.status_code == 200
    assert 'longitude' in response.json()
    if longitude == 180.0 or longitude == -180.0:
        assert (response.json()['longitude'] == pytest.approx(180.0, abs=0.1)) or (response.json()['longitude'] == pytest.approx(-180.0, abs=0.1))
    else:
        assert response.json()['longitude'] == pytest.approx(longitude, abs=0.1)

# Test cases for invalid longitude values
@pytest.mark.parametrize("longitude", [-180.1, 180.1, -181.0, 181.0, -200.0, 200.0])
def test_invalid_longitude(longitude):
    response = get_weather_data(longitude)
    assert response.status_code == 400
    assert 'error' in response.json()
    assert response.json()['error'] == True
    assert response.json()['reason'] == f"Longitude must be in range of -180 to 180°. Given: {longitude}."

# Function to retrieve weather data from the API
def get_weather_data(longitude):
    url = f"https://api.open-meteo.com/v1/forecast?latitude=0&longitude={longitude}&hourly=temperature_2m"
    response = requests.get(url)
    return response