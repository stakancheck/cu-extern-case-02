import requests
from typing import Dict, NoReturn

from pydantic import ValidationError


import logging

from config import Config
from ..models.geocoding_model import GeocodingResponse


class GeocodingAPIException(Exception):
    """Custom exception for geocoding API errors"""
    pass


class GeocodingAPICityNotFound(GeocodingAPIException):
    """Custom exception for geocoding API if city not found"""


class GeocodingService:
    def __init__(self):
        self.base_url = "https://api.openweathermap.org/geo/1.0"
        self.api_key = Config.OPENWEATHER_API_KEY

    def _make_request(self, endpoint: str, params: Dict) -> Dict | NoReturn:
        """Make request to OpenWeather Geocoding API"""
        try:
            params['appid'] = self.api_key
            response = requests.get(f"{self.base_url}/{endpoint}", params=params)
            response.raise_for_status()
            return response.json()

        except requests.RequestException as e:
            logging.error(f"API request failed: {str(e)}")
            raise GeocodingAPIException(f"Failed to fetch geocoding data: {str(e)}")

    def get_coordinates_by_city_name(self, city_name: str) -> GeocodingResponse | NoReturn:
        """Get coordinates for a given city name"""
        params = {
            'q': city_name,
            'limit': 1
        }

        data = self._make_request('direct', params)

        if not data:
            raise GeocodingAPICityNotFound(f"No data found for city: {city_name}")

        try:
            weather_data = GeocodingResponse(**(data[0]))
            return weather_data
        except ValidationError as e:
            raise ValueError(f"Data validation error: {e.errors()}")


if __name__ == '__main__':
    # Sample test
    service = GeocodingService()
    result = service.get_coordinates_by_city_name("Рим")
    print(result)
