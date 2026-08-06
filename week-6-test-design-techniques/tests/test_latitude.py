import pytest
import requests

# Latitude tests for https://open-meteo.com

# Equivalence Class Partitioning (ECP) - classes:
# 1. Valid latitude values: -90 to 90
# 2. Invalid latitude values: less than -90 or greater than 90

# Boundary Value Analysis (BVA) - boundaries:
# 1. Lower boundary: -90
# 2. Upper boundary: 90
# 3. Just below lower boundary: -90.1
# 4. Just above upper boundary: 90.1

# Test cases for valid latitude values

@pytest.mark.parametrize("latitude", [-90.0, -45.0, 0.0, 45.0, 90.0])
def test_valid_latitude(latitude):
    response = get_weather_data(latitude)
    assert response.status_code == 200
    assert 'latitude' in response.json()
    assert response.json()['latitude'] == pytest.approx(latitude, abs=0.1)


# Test cases for invalid latitude values
@pytest.mark.parametrize("latitude", [90.1, -90.1, -91.0, 91.0, -100.0, 100.0])
def test_invalid_latitude(latitude):
    response = get_weather_data(latitude)
    assert response.status_code == 400
    assert 'error' in response.json()
    assert response.json()['error'] == True
    assert response.json()['reason'] == f"Latitude must be in range of -90 to 90°. Given: {latitude}."

# Function to retrieve weather data from the API 
def get_weather_data(latitude):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude=0&hourly=temperature_2m"
    response = requests.get(url)
    return response
