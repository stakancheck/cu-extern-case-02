from flask import Blueprint, render_template, current_app, request, jsonify
from flask_babel import gettext as _, get_locale
from ..services.plot_service import create_weather_plot_temp, create_weather_plot_wind
from ..services.weather_analyzer_service import WeatherAnalyzerService
from ..services.weather_service import WeatherService

weather_bp = Blueprint('weather', __name__)

@weather_bp.route('/weather', methods=['GET', 'POST'])
def weather():
    try:
        if request.method == 'POST':
            data = request.get_json()
            cities = data.get('cities', [])

            if not cities:
                return render_template('weather.html')

            weather_service = WeatherService()
            analyzer = WeatherAnalyzerService()
            cities_weather = []

            for city in cities:
                # Get weather data for the city
                weather_data = weather_service.get_weather_by_city(city, str(get_locale()))
                hourly_weather_data = weather_service.get_weather_hourly_by_city(city, str(get_locale()))

                # Analyze weather conditions for the city
                warning = analyzer.analyze_weather(weather_data)

                # Format data for display for the city
                weather_info = {
                    'city': weather_data.name,
                    'temperature': round(weather_data.main.temp),
                    'feels_like': round(weather_data.main.feels_like),
                    'description': weather_data.weather[0].description,
                    'humidity': weather_data.main.humidity,
                    'wind_speed': round(weather_data.wind.speed),
                    'pressure': weather_data.main.pressure,
                    'warning': warning,
                    'hourly_weather': hourly_weather_data.list
                }

                # Extract data for plotting
                dates = [entry.pretty_dt for entry in hourly_weather_data.list]
                temperatures = [entry.main.temp for entry in hourly_weather_data.list]
                wind_speeds = [entry.wind.speed for entry in hourly_weather_data.list]

                # Create plot
                weather_info['plot_url_temp'] = create_weather_plot_temp(dates, temperatures)
                weather_info['plot_url_wind'] = create_weather_plot_wind(dates, wind_speeds)

                cities_weather.append(weather_info)

            return render_template('weather.html', cities_weather=cities_weather)

        # Если метод GET, просто отобразить пустую форму
        return render_template('weather.html')

    except Exception as e:
        current_app.logger.error(f"Error in weather route: {e}")
        return render_template('weather.html', error=_("Unable to fetch weather data"))
