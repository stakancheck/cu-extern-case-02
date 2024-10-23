import unittest
from unittest.mock import patch, Mock

import requests

from app.services.geocoding_service import GeocodingService, GeocodingAPIException, GeocodingAPICityNotFound
from app.services.weather_service import WeatherService, WeatherAPIException
from models import OpenWeatherResponse


class TestWeatherService(unittest.TestCase):
    def setUp(self):
        self.weather_service = WeatherService()

    @patch('app.services.weather_service.requests.get')
    def test_get_weather_by_coordinates_api_failure(self, mock_get):
        # Mock the API response to raise an exception
        mock_get.side_effect = requests.RequestException("API request failed")

        with self.assertRaises(WeatherAPIException):
            self.weather_service.get_weather_by_coordinates(35, 139)

    @patch('app.services.weather_service.requests.get')
    def test_get_weather_by_coordinates_validation_error(self, mock_get):
        # Mock the API response with invalid data
        mock_response = Mock()
        mock_response.json.return_value = {}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        with self.assertRaises(ValueError):
            self.weather_service.get_weather_by_coordinates(35, 139)

    @patch('app.services.weather_service.GeocodingService.get_coordinates_by_city_name')
    @patch('app.services.weather_service.WeatherService.get_weather_by_coordinates')
    def test_get_weather_by_city_success(self, mock_get_weather_by_coordinates, mock_get_coordinates_by_city_name):
        mock_geocoding_response = Mock()
        mock_geocoding_response.lat = 55.7504461
        mock_geocoding_response.lon = 37.6174943
        mock_get_coordinates_by_city_name.return_value = mock_geocoding_response

        mock_weather_response = Mock(spec=OpenWeatherResponse)
        mock_get_weather_by_coordinates.return_value = mock_weather_response

        result = self.weather_service.get_weather_by_city("Moscow")
        self.assertEqual(result, mock_weather_response)
        mock_get_coordinates_by_city_name.assert_called_once_with("Moscow")
        mock_get_weather_by_coordinates.assert_called_once_with(55.7504461, 37.6174943, 'en')

    @patch('app.services.weather_service.GeocodingService.get_coordinates_by_city_name')
    def test_get_weather_by_city_non_existent_city(self, mock_get_coordinates_by_city_name):
        mock_get_coordinates_by_city_name.side_effect = GeocodingAPICityNotFound("City not found")

        with self.assertRaises(GeocodingAPICityNotFound):
            self.weather_service.get_weather_by_city("NonExistentCity")

    @patch('app.services.weather_service.GeocodingService.get_coordinates_by_city_name')
    @patch('app.services.weather_service.WeatherService.get_weather_by_coordinates')
    def test_get_weather_by_city_api_failure(self, mock_get_weather_by_coordinates, mock_get_coordinates_by_city_name):
        mock_geocoding_response = Mock()
        mock_geocoding_response.lat = 55.7504461
        mock_geocoding_response.lon = 37.6174943
        mock_get_coordinates_by_city_name.return_value = mock_geocoding_response

        mock_get_weather_by_coordinates.side_effect = WeatherAPIException("API request failed")

        with self.assertRaises(WeatherAPIException):
            self.weather_service.get_weather_by_city("Moscow")


class TestGeocodingService(unittest.TestCase):

    @patch('app.services.geocoding_service.requests.get')
    def test_get_coordinates_by_city_name_moscow(self, mock_get):
        mock_response = {
            "name": "Moscow",
            "local_names": {
                "en": "Moscow",
                "ru": "Москва"
            },
            "lat": 55.7504461,
            "lon": 37.6174943,
            "country": "RU",
            "state": "Moscow"
        }
        mock_get.return_value.json.return_value = [mock_response]
        mock_get.return_value.raise_for_status = lambda: None

        service = GeocodingService()
        result = service.get_coordinates_by_city_name("Moscow")
        self.assertEqual(result.name, "Moscow")

    @patch('app.services.geocoding_service.requests.get')
    def test_get_coordinates_by_city_name_moskva(self, mock_get):
        mock_response = {
            "name": "Moscow",
            "local_names": {
                "en": "Moscow",
                "ru": "Москва"
            },
            "lat": 55.7504461,
            "lon": 37.6174943,
            "country": "RU",
            "state": "Moscow"
        }
        mock_get.return_value.json.return_value = [mock_response]
        mock_get.return_value.raise_for_status = lambda: None

        service = GeocodingService()
        result = service.get_coordinates_by_city_name("Москва")
        self.assertEqual(result.name, "Moscow")

    @patch('app.services.geocoding_service.requests.get')
    def test_get_coordinates_by_city_name_no_local_names(self, mock_get):
        mock_response = {
            "name": "Moscow",
            "lat": 55.7504461,
            "lon": 37.6174943,
            "country": "RU",
            "state": "Moscow"
        }
        mock_get.return_value.json.return_value = [mock_response]
        mock_get.return_value.raise_for_status = lambda: None

        service = GeocodingService()
        result = service.get_coordinates_by_city_name("Mokva")
        self.assertEqual(result.name, "Moscow")
        self.assertIsNone(result.local_names)

    @patch('app.services.geocoding_service.requests.get')
    def test_get_coordinates_by_city_name_non_existent(self, mock_get):
        mock_get.return_value.json.return_value = []
        mock_get.return_value.raise_for_status = lambda: None

        service = GeocodingService()
        with self.assertRaises(GeocodingAPIException):
            service.get_coordinates_by_city_name("NonExistentCity")


if __name__ == '__main__':
    unittest.main()
