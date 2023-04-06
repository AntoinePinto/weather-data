import numpy as np
import requests

ARCHIVE_URL = "https://archive-api.open-meteo.com/v1/era5"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

def get_latest_recorded_date():
    """
    Returns the latest recorded date in the weather archive database.

    Returns:
    str: The latest recorded date in YYYY-MM-DD format.
    """
    filter = f"latitude=0&longitude=0&start_date=2023-01-01&end_date=2030-12-31"
    r = requests.get(ARCHIVE_URL + '?' + filter)
    latest_recorded_date = r.json()['reason'][-10:]

    return latest_recorded_date

def get_archived_weather(lat, long, start, end, metrics):
    """
    Returns historical weather data for a given latitude and longitude, time range, and set of metrics.

    Args:
    lat (float): Latitude of location.
    long (float): Longitude of location.
    start (str): Start date in YYYY-MM-DD format.
    end (str): End date in YYYY-MM-DD format.
    metrics (list): List of weather metrics to retrieve (https://open-meteo.com/en/docs for more details).

    Returns:
    dict: Dictionary containing weather data, with latitude and longitude as separate keys and weather metrics as sub-dictionaries.
    """
    metrics = ','.join(metrics)
    filter = f'latitude={lat}&longitude={long}&hourly={metrics}&start_date={start}&end_date={end}'
    r = requests.get(ARCHIVE_URL + '?' + filter)
    d = r.json()

    return {**{'latitude': d['latitude'], 'longitude': d['longitude']}, **d['hourly']}

def get_forecast_weather(lat, long, metrics):
    """
    Returns forecasted weather data for a given latitude and longitude and set of metrics.

    Args:
    lat (float): Latitude of location.
    long (float): Longitude of location.
    metrics (list): List of weather metrics to retrieve (e.g. ['temperature', 'precipitation']).

    Returns:
    dict: Dictionary containing weather data, with latitude and longitude as separate keys and weather metrics as sub-dictionaries.
    """
    metrics = ','.join(metrics)
    filter = f'latitude={lat}&longitude={long}&hourly={metrics}'
    r = requests.get(FORECAST_URL + '?' + filter)
    d = r.json()

    return {**{'latitude': d['latitude'], 'longitude': d['longitude']}, **d['hourly']}

def get_distance(lon1, lat1, lon2, lat2):
    """
    Returns the distance, in kilometers, between two sets of longitude/latitude coordinates.

    Args:
    lon1 (float): Longitude of first location.
    lat1 (float): Latitude of first location.
    lon2 (float): Longitude of second location.
    lat2 (float): Latitude of second location.

    Returns:
    float: The distance, in kilometers, between the two sets of coordinates.
    """
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])
    newlon = lon2 - lon1
    newlat = lat2 - lat1

    haver_formula = np.sin(newlat/2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(newlon/2.0)**2
    km = 6367 * 2 * np.arcsin(np.sqrt(haver_formula ))

    return km