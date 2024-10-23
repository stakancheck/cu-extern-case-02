import logging
from pprint import pprint
from typing import Dict, NoReturn

import requests
from pydantic import ValidationError

from config import Config
from models import OpenWeatherResponse
from services.geocoding_service import GeocodingService, GeocodingAPIException, GeocodingAPICityNotFound


class WeatherAPIException(Exception):
    """Custom exception for weather API errors"""
    pass


class WeatherService:
    def __init__(self):
        self.base_url = "https://api.openweathermap.org/data/2.5"
        self.api_key = Config.OPENWEATHER_API_KEY

    def _make_request(self, endpoint: str, params: Dict) -> Dict | NoReturn:
        """Make request to OpenWeather API"""
        try:
            params['appid'] = self.api_key
            response = requests.get(f"{self.base_url}/{endpoint}", params=params)
            response.raise_for_status()
            return response.json()

        except requests.RequestException as e:
            logging.error(f"API request failed: {str(e)}")
            raise WeatherAPIException(f"Failed to fetch weather data: {str(e)}")

    def get_weather_by_coordinates(self, lat: float, lon: float) -> OpenWeatherResponse | NoReturn:
        """Get current weather for given coordinates"""
        params = {
            'lat': lat,
            'lon': lon,
            'units': 'metric'  # Для получения температуры в Цельсиях
        }

        data = self._make_request('weather', params)

        try:
            weather_data = OpenWeatherResponse(**data)
            return weather_data
        except ValidationError as e:
            raise ValueError(f"Data validation error: {e.errors()}")

    def get_weather_by_city(self, city_name: str) -> OpenWeatherResponse | NoReturn:
        """Get weather data for a given city name"""
        geocoding_service = GeocodingService()
        try:
            geocoding_response = geocoding_service.get_coordinates_by_city_name(city_name)
            lat = geocoding_response.lat
            lon = geocoding_response.lon
            return self.get_weather_by_coordinates(lat, lon)
        except GeocodingAPICityNotFound as e:
            logging.error(f"Can't found city with name {city_name}: {str(e)}")
            raise GeocodingAPICityNotFound(f"No data found for city: {city_name}")
        except (GeocodingAPIException, ValueError) as e:
            logging.error(f"Failed to get weather data for city {city_name}: {str(e)}")
            raise GeocodingAPIException(f"Failed to get weather data for city {city_name}: {str(e)}")


if __name__ == '__main__':
    # Sample test
    service = WeatherService()
    result = service.get_weather_by_coordinates(42.785780, 12.027960)
    pprint(result)
