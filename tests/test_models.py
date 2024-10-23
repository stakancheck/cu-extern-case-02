import unittest
from unittest.mock import Mock

from app.services.weather_analyzer_service import WeatherAnalyzerService, WeatherSeverity, WeatherWarning
from models import OpenWeatherResponse, Main, Wind, Rain, Snow


class TestWeatherAnalyzerService(unittest.TestCase):
    def setUp(self):
        self.analyzer = WeatherAnalyzerService()

    def test_analyze_weather_normal_conditions(self):
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
        weather_data = OpenWeatherResponse(
            main=Main(temp=20.0, feels_like=20.0, pressure=1013, humidity=50),
            wind=Wind(speed=5.0),
            rain = Rain(**{'1h': 35.0}),
            snow=None,
            visibility=10000
        )
        result = self.analyzer.analyze_weather(weather_data)
        self.assertEqual(result.severity, WeatherSeverity.EXTREME)
        self.assertIn("extreme_rain", result.conditions)

    def test_analyze_weather_extreme_rain(self):
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


if __name__ == '__main__':
    unittest.main()
