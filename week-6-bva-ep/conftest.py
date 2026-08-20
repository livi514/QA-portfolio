import requests

BASE_URL = "https://api.open-meteo.com/v1/forecast"


def get_weather_data(latitude=0, longitude=0, start_date=None, end_date=None):
    """
    Shared request helper for the Week 6 BVA/ECP suite.

    Centralising this means the base URL and query construction only live
    in one place -- previously test_dates.py, test_latitude.py, and
    test_longitude.py each had their own near-identical copy, each hardcoding
    the same base URL.

    latitude/longitude default to 0 so callers testing only dates don't need
    to pass them, and callers testing only latitude/longitude don't need to
    pass date params (Open-Meteo returns current-day data when no start/end
    date is given, which is fine for lat/long boundary checks).
    """
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "temperature_2m",
    }
    if start_date is not None:
        params["start_date"] = start_date
    if end_date is not None:
        params["end_date"] = end_date

    return requests.get(BASE_URL, params=params)
