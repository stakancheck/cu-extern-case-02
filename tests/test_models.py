import unittest
from datetime import datetime, timedelta
from unittest.mock import Mock, patch

import pytz

from app.services.weather_analyzer_service import WeatherAnalyzerService, WeatherSeverity, WeatherWarning
from models import OpenWeatherResponse, Main, Wind, Rain, Snow, OpenWeatherHourlyResponse, Coord, WeatherConditionsList


class TestWeatherAnalyzerService(unittest.TestCase):
    def setUp(self):
        self.analyzer = WeatherAnalyzerService()

    def test_analyze_weather_normal_conditions(self):
        from models import OpenWeatherResponse, Main, Wind
        weather_data = OpenWeatherResponse(
            main=Main(temp=20.0, feels_like=20.0, pressure=1013, humidity=50),
            wind=Wind(speed=5.0),
            rain=None,
            snow=None,
            visibility=10000
        )
        result = self.analyzer.analyze_weather(weather_data)
        self.assertEqual(result.severity, WeatherSeverity.NORMAL)
        self.assertEqual(result.description, "Weather conditions are normal.")
        self.assertEqual(result.conditions, [])

    def test_analyze_weather_extreme_cold(self):
        from models import OpenWeatherResponse, Main, Wind
        weather_data = OpenWeatherResponse(
            main=Main(temp=-15.0, feels_like=-15.0, pressure=1013, humidity=50),
            wind=Wind(speed=5.0),
            rain=None,
            snow=None,
            visibility=10000
        )
        result = self.analyzer.analyze_weather(weather_data)
        self.assertEqual(result.severity, WeatherSeverity.SEVERE)
        self.assertIn("extreme_cold", result.conditions)

    def test_analyze_weather_extreme_heat(self):
        from models import OpenWeatherResponse, Main, Wind
        weather_data = OpenWeatherResponse(
            main=Main(temp=35.0, feels_like=35.0, pressure=1013, humidity=50),
            wind=Wind(speed=5.0),
            rain=None,
            snow=None,
            visibility=10000
        )
        result = self.analyzer.analyze_weather(weather_data)
        self.assertEqual(result.severity, WeatherSeverity.SEVERE)
        self.assertIn("extreme_heat", result.conditions)

    def test_analyze_weather_strong_wind(self):
        from models import OpenWeatherResponse, Main, Wind
        weather_data = OpenWeatherResponse(
            main=Main(temp=20.0, feels_like=20.0, pressure=1013, humidity=50),
            wind=Wind(speed=12.0),
            rain=None,
            snow=None,
            visibility=10000
        )
        result = self.analyzer.analyze_weather(weather_data)
        self.assertEqual(result.severity, WeatherSeverity.SEVERE)
        self.assertIn("strong_wind", result.conditions)

    def test_analyze_weather_extreme_wind(self):
        from models import OpenWeatherResponse, Main, Wind
        weather_data = OpenWeatherResponse(
            main=Main(temp=20.0, feels_like=20.0, pressure=1013, humidity=50),
            wind=Wind(speed=16.0),
            rain=None,
            snow=None,
            visibility=10000
        )
        result = self.analyzer.analyze_weather(weather_data)
        self.assertEqual(result.severity, WeatherSeverity.EXTREME)
        self.assertIn("extreme_wind", result.conditions)

    def test_analyze_weather_heavy_rain(self):
        from models import OpenWeatherResponse, Main, Wind, Rain
        weather_data = OpenWeatherResponse(
            main=Main(temp=20.0, feels_like=20.0, pressure=1013, humidity=50),
            wind=Wind(speed=5.0),
            rain=Rain(**{'1h': 35.0}),
            snow=None,
            visibility=10000
        )
        result = self.analyzer.analyze_weather(weather_data)
        self.assertEqual(result.severity, WeatherSeverity.EXTREME)
        self.assertIn("extreme_rain", result.conditions)

    def test_analyze_weather_extreme_rain(self):
        from models import OpenWeatherResponse, Main, Wind, Rain
        weather_data = OpenWeatherResponse(
            main=Main(temp=20.0, feels_like=20.0, pressure=1013, humidity=50),
            wind=Wind(speed=5.0),
            rain=Rain(**{'1h': 35.0}),
            snow=None,
            visibility=10000
        )
        result = self.analyzer.analyze_weather(weather_data)
        print(result)
        self.assertEqual(result.severity, WeatherSeverity.EXTREME)
        self.assertIn("extreme_rain", result.conditions)

    def test_analyze_weather_heavy_snow(self):
        from models import OpenWeatherResponse, Main, Wind, Snow
        weather_data = OpenWeatherResponse(
            main=Main(temp=20.0, feels_like=20.0, pressure=1013, humidity=50),
            wind=Wind(speed=5.0),
            rain=None,
            snow=Snow(**{'1h': 15.0}),
            visibility=10000
        )
        result = self.analyzer.analyze_weather(weather_data)
        self.assertEqual(result.severity, WeatherSeverity.SEVERE)
        self.assertIn("heavy_snow", result.conditions)

    def test_analyze_weather_extreme_snow(self):
        from models import OpenWeatherResponse, Main, Wind, Snow
        weather_data = OpenWeatherResponse(
            main=Main(temp=20.0, feels_like=20.0, pressure=1013, humidity=50),
            wind=Wind(speed=5.0),
            rain=None,
            snow=Snow(**{'1h': 25.0}),
            visibility=10000
        )
        result = self.analyzer.analyze_weather(weather_data)
        self.assertEqual(result.severity, WeatherSeverity.EXTREME)
        self.assertIn("extreme_snow", result.conditions)

    def test_analyze_weather_poor_visibility(self):
        from models import OpenWeatherResponse, Main, Wind
        weather_data = OpenWeatherResponse(
            main=Main(temp=20.0, feels_like=20.0, pressure=1013, humidity=50),
            wind=Wind(speed=5.0),
            rain=None,
            snow=None,
            visibility=500
        )
        result = self.analyzer.analyze_weather(weather_data)
        self.assertEqual(result.severity, WeatherSeverity.SEVERE)
        self.assertIn("poor_visibility", result.conditions)

    @patch('app.models.openweather_model.WeatherAnalyzerService.analyze_weather')
    def test_from_openweather_hourly_response(self, mock_analyze_weather):
        from models import OpenWeatherHourlyResponse, OpenWeatherResponse, Coord, Main, Wind, City, \
            WeatherConditionsList
        # Mock the analyze_weather method to return a predefined warning
        mock_analyze_weather.return_value = WeatherWarning(
            severity=WeatherSeverity.NORMAL,
            conditions=[],
            description="Weather conditions are normal."
        )

        # Create a mock OpenWeatherHourlyResponse
        hourly_response = OpenWeatherHourlyResponse(
            cod="200",
            list=[
                OpenWeatherResponse(
                    coord=Coord(lon=37.6174943, lat=55.7504461),
                    main=Main(temp=15.0, feels_like=14.0, pressure=1012, humidity=50),
                    visibility=10000,
                    wind=Wind(speed=3.0, deg=200),
                    dt=1605182400,
                    timezone=10800
                )
            ],
            city=City(
                id=524901,
                name="Moscow",
                coord=Coord(lon=37.6174943, lat=55.7504461),
                country="RU",
                population=0,
                timezone=10800,
                sunrise=1605154852,
                sunset=1605184952
            )
        )

        # Call the method under test
        weather_conditions_list = WeatherConditionsList.from_openweather_hourly_response(hourly_response)

        # Assert the results
        self.assertEqual(len(weather_conditions_list.conditions), 1)
        weather_condition = weather_conditions_list.conditions[0]
        self.assertEqual(weather_condition.dt,
                         datetime.fromtimestamp(1605182400).replace(tzinfo=pytz.utc) + timedelta(seconds=10800))
        self.assertEqual(weather_condition.wind_speed, 3.0)
        self.assertEqual(weather_condition.wind_deg, 200)
        self.assertEqual(weather_condition.temp, 15.0)
        self.assertEqual(weather_condition.feels_like, 14.0)
        self.assertEqual(weather_condition.precipitation, None)
        self.assertEqual(weather_condition.visibility, 10000)
        self.assertEqual(weather_condition.warning.severity, WeatherSeverity.NORMAL)
        self.assertEqual(weather_condition.warning.description, "Weather conditions are normal.")


if __name__ == '__main__':
    unittest.main()
