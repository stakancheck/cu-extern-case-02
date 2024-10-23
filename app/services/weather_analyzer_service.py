from dataclasses import dataclass
from enum import Enum
from typing import Optional, List

from flask_babel import gettext as _
from pydantic import BaseModel

from ..models import OpenWeatherResponse
from .weather_service import WeatherService


class WeatherSeverity(Enum):
    NORMAL = "normal"
    SEVERE = "severe"
    EXTREME = "extreme"


@dataclass
class WeatherThresholds:
    # Пороговые значения для определения неблагоприятных условий
    temp_min: float = -10.0
    temp_max: float = 30.0
    wind_speed_severe: float = 10.0  # м/с
    wind_speed_extreme: float = 15.0  # м/с
    rain_severe: float = 15.0  # мм/час
    rain_extreme: float = 30.0  # мм/час
    snow_severe: float = 10.0  # мм/час
    snow_extreme: float = 20.0  # мм/час
    visibility_poor: int = 800  # метров


class WeatherWarning(BaseModel):
    severity: WeatherSeverity
    conditions: List[str]
    description: str


class WeatherAnalyzerService:
    def __init__(self, thresholds: Optional[WeatherThresholds] = None):
        self.thresholds = thresholds or WeatherThresholds()

    @staticmethod
    def _get_severity_description(severity: WeatherSeverity) -> str:
        descriptions = {
            WeatherSeverity.NORMAL: _("Weather conditions are normal."),
            WeatherSeverity.SEVERE: _("Caution: Adverse weather conditions detected."),
            WeatherSeverity.EXTREME: _("Warning: Extreme weather conditions detected!")
        }
        return descriptions[severity]

    @staticmethod
    def _get_condition_description(condition: str) -> str:
        condition_descriptions = {
            "extreme_cold": _("Extremely low temperature"),
            "extreme_heat": _("Extremely high temperature"),
            "strong_wind": _("Strong wind"),
            "extreme_wind": _("Dangerous wind speed"),
            "heavy_rain": _("Heavy rain"),
            "extreme_rain": _("Extremely heavy rain"),
            "heavy_snow": _("Heavy snow"),
            "extreme_snow": _("Extremely heavy snow"),
            "poor_visibility": _("Poor visibility conditions")
        }
        return condition_descriptions.get(condition, "")

    def analyze_weather(self, weather_data: OpenWeatherResponse) -> WeatherWarning:
        conditions = []
        severity = WeatherSeverity.NORMAL

        # Проверка температуры
        if weather_data.main.temp < self.thresholds.temp_min:
            conditions.append("extreme_cold")
            severity = WeatherSeverity.SEVERE
        elif weather_data.main.temp > self.thresholds.temp_max:
            conditions.append("extreme_heat")
            severity = WeatherSeverity.SEVERE

        # Проверка ветра
        if weather_data.wind.speed >= self.thresholds.wind_speed_extreme:
            conditions.append("extreme_wind")
            severity = WeatherSeverity.EXTREME
        elif weather_data.wind.speed >= self.thresholds.wind_speed_severe:
            conditions.append("strong_wind")
            severity = WeatherSeverity.SEVERE

        # Проверка осадков
        if weather_data.rain and weather_data.rain.one_h:
            if weather_data.rain.one_h >= self.thresholds.rain_extreme:
                conditions.append("extreme_rain")
                severity = WeatherSeverity.EXTREME
            elif weather_data.rain.one_h >= self.thresholds.rain_severe:
                conditions.append("heavy_rain")
                severity = WeatherSeverity.SEVERE

        if weather_data.snow and weather_data.snow.one_h:
            if weather_data.snow.one_h >= self.thresholds.snow_extreme:
                conditions.append("extreme_snow")
                severity = WeatherSeverity.EXTREME
            elif weather_data.snow.one_h >= self.thresholds.snow_severe:
                conditions.append("heavy_snow")
                severity = WeatherSeverity.SEVERE

        # Проверка видимости
        if weather_data.visibility and weather_data.visibility <= self.thresholds.visibility_poor:
            conditions.append("poor_visibility")
            severity = WeatherSeverity.SEVERE

        # Формируем детальное описание
        detailed_conditions = [self._get_condition_description(cond) for cond in conditions]
        description = self._get_severity_description(severity)
        if detailed_conditions:
            conditions_text = ", ".join(detailed_conditions)
            description = f"{description}\n{_('Detected conditions')}: {conditions_text}"

        return WeatherWarning(
            severity=severity,
            conditions=conditions,
            description=description
        )


if __name__ == '__main__':
    # Sample test
    weather_service = WeatherService()
    weather_analyzer_service = WeatherAnalyzerService()
    weather = weather_service.get_weather_by_city('Tanger')
    print(weather)
    analyzed_weather = weather_analyzer_service.analyze_weather(weather)
    print(analyzed_weather)
