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
#
# NOTE on -90.0001 / 90.0001: these deltas assume the API rejects rather than
# rounds/clamps a value this close to the boundary. Worth confirming manually
# once (e.g. curl the endpoint at -90.0001) before trusting this as a genuine
# invalid-boundary test rather than a false negative from silent rounding.


def get_weather_data(latitude):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude=0&hourly=temperature_2m"
    return requests.get(url)


# Valid latitude values (ECP + BVA)
@pytest.mark.parametrize("latitude", [-90.0, -89.9, -45.0, 0.0, 45.0, 89.9, 90.0])
def test_valid_latitude(latitude):
    response = get_weather_data(latitude)
    assert response.status_code == 200
    assert "latitude" in response.json()
    # API returns floats with slight rounding differences
    assert response.json()["latitude"] == pytest.approx(latitude, abs=0.1)


# Invalid latitude values (ECP + BVA)
#
# FIX: previously hard-asserted status_code == 400 and error/reason keys
# being present. The longitude suite already discovered the API sometimes
# returns 503 for invalid values, with no guaranteed error/reason payload --
# there's no reason to assume latitude is immune, and hard-asserting 400 here
# risks an intermittent failure that isn't a real regression, just an
# unhandled case you'd already solved elsewhere. Mirrors the longitude fix.
@pytest.mark.parametrize("latitude", [-90.0001, -91.0, -100.0, 90.0001, 91.0, 100.0])
def test_invalid_latitude(latitude):
    response = get_weather_data(latitude)

    # API may return 400 or 503 depending on internal routing
    assert response.status_code in (400, 503)

    # Error field may not exist on 503 responses
    reason = response.json().get("reason", "")
    assert "Latitude must be in range" in reason