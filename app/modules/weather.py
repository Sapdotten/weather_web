import openmeteo_requests

import requests_cache
import pandas as pd
from retry_requests import retry
import logging
from typing import Union
from datetime import datetime, timedelta


class WeatherHelper:
    URL = "https://api.open-meteo.com/v1/forecast"
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)
    weather_params = ["temperature_2m_max",
                      "temperature_2m_min",
                      "precipitation_probability_mean",
                      "wind_speed_10m_max",
                      "wind_gusts_10m_max"
                      ]
    day_weather_params = ["temperature_2m",
                          "precipitation_probability",
                          "wind_speed_10m",
                          "wind_gusts_10m",
                          ]

    @classmethod
    def get_weather_week(cls, coords: list[float]) -> Union[dict[str, float], None]:
        params = {
            "latitude": coords[0],
            "longitude": coords[1],
            "daily": cls.weather_params
        }
        try:
            response = cls.openmeteo.weather_api(
                cls.URL, params=params)[0].Daily()
        except Exception as e:
            logging.warning(f"Something went wrong in try to get weather: {e}")
            return None

        cast = []
        _time = response.Time()
        _time = datetime.fromtimestamp(_time)
        for day in range(0, 7):
            cast.append({})
            cast[day]['day'] = _time.strftime('%d.%m')
            _time = _time+timedelta(seconds=response.Interval())
        for index, weather_param in enumerate(cls.weather_params):
            values = list(
                response.Variables(index).ValuesAsNumpy())
            for day, value in enumerate(values):
                cast[day][weather_param] = int(float(value))

        return cast

    @classmethod
    def get_weather_today(cls, coords: list[float]) -> Union[list[dict[str, float]], None]:
        params = {
            "latitude": coords[0],
            "longitude": coords[1],
            "current_weather": True,
            "hourly": cls.day_weather_params
        }
        response = cls.openmeteo.weather_api(
            cls.URL, params=params)[0]
        current_weather = response.Current()
        hourly_weather = response.Hourly()

        weather_data = [
            {
                "temperature": current_weather.Variables(0).ValuesAsNumpy(),
                "windspeed": int(float(current_weather.Variables(2).ValuesAsNumpy())),
                "windgust": int(float(current_weather.Variables(3).ValuesAsNumpy())),
                "precipitation_probability": int(float(current_weather.Variables(1).ValuesAsNumpy()))
            }
        ]

        for i in range(1, 6):
            weather_data.append({
                "temperature": hourly_weather.Variables(0).ValuesAsNumpy(),
                "windspeed": hourly_weather.Variables(2).ValuesAsNumpy(),
                "windgust": hourly_weather.Variables(3).ValuesAsNumpy(),
                "precipitation_probability": hourly_weather.Variables(1
                                                                      ).ValuesAsNumpy()
            })

        return weather_data
