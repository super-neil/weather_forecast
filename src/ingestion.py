# src/ingestion.py
import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry

def get_openmeteo_client():
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    return openmeteo_requests.Client(session=retry_session)

def fetch_weather_data(lat, long, start_date, end_date):
    client = get_openmeteo_client()
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": lat,
        "longitude": long,
        "start_date": start_date,
        "end_date": end_date,
        "daily": ["temperature_2m_max", "precipitation_sum", "wind_speed_10m_max", "relative_humidity_2m_mean", "pressure_msl_mean", "cloud_cover_mean" ],
        "timezone": "Europe/London"
    }

    responses = client.weather_api(url, params=params)
    response = responses[0]
    elevation = response.Elevation()
    daily = response.Daily()

    df = pd.DataFrame({
        "temp": daily.Variables(0).ValuesAsNumpy(),
        "rain": daily.Variables(1).ValuesAsNumpy(),
        "wind": daily.Variables(2).ValuesAsNumpy(),
        "humid": daily.Variables(3).ValuesAsNumpy(),
        "pressure": daily.Variables(4).ValuesAsNumpy(),
        "cloud": daily.Variables(5).ValuesAsNumpy()        
    })
    
    # Metadata
    df['lat'] = lat
    df['long'] = long
    df['elevation'] = elevation
    
    # Time Index
    df['date'] = pd.date_range(
        start=pd.to_datetime(daily.Time(), unit="s", utc=True),
        end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),
        freq=pd.Timedelta(seconds=daily.Interval()),
        inclusive="left"
    )
    return df