from flask import Blueprint, render_template, current_app, request
from flask_babel import gettext as _, get_locale

from ..services.plot_service import create_weather_plot_temp, create_weather_plot_wind
from ..services.weather_analyzer_service import WeatherAnalyzerService
from ..services.weather_service import WeatherService

weather_bp = Blueprint('weather', __name__)

@weather_bp.route('/weather')
def weather():
    try:
        start_city = request.args.get('start_city')
        end_city = request.args.get('end_city')

        if not start_city or not end_city:
            return render_template('weather.html')

        # Get weather data for the start city
        weather_service = WeatherService()
        start_weather_data = weather_service.get_weather_by_city(start_city, str(get_locale()))
        start_hourly_weather_data = weather_service.get_weather_hourly_by_city(start_city, str(get_locale()))

        # Analyze weather conditions for the start city
        analyzer = WeatherAnalyzerService()
        start_warning = analyzer.analyze_weather(start_weather_data)

        # Format data for display for the start city
        start_weather_info = {
            'city': start_weather_data.name,
            'temperature': round(start_weather_data.main.temp),
            'feels_like': round(start_weather_data.main.feels_like),
            'description': start_weather_data.weather[0].description,
            'humidity': start_weather_data.main.humidity,
            'wind_speed': round(start_weather_data.wind.speed),
            'pressure': start_weather_data.main.pressure,
        }

        # Get weather data for the end city
        end_weather_data = weather_service.get_weather_by_city(end_city, str(get_locale()))
        end_hourly_weather_data = weather_service.get_weather_hourly_by_city(end_city, str(get_locale()))

        # Analyze weather conditions for the end city
        end_warning = analyzer.analyze_weather(end_weather_data)

        # Format data for display for the end city
        end_weather_info = {
            'city': end_weather_data.name,
            'temperature': round(end_weather_data.main.temp),
            'feels_like': round(end_weather_data.main.feels_like),
            'description': end_weather_data.weather[0].description,
            'humidity': end_weather_data.main.humidity,
            'wind_speed': round(end_weather_data.wind.speed),
            'pressure': end_weather_data.main.pressure,
        }

        # Extract data for plotting
        dates = [entry.pretty_dt for entry in start_hourly_weather_data.list]
        temperatures = [entry.main.temp for entry in start_hourly_weather_data.list]
        wind_speeds = [entry.wind.speed for entry in start_hourly_weather_data.list]

        # Create plot
        plot_url_temp = create_weather_plot_temp(dates, temperatures)
        plot_url_wind = create_weather_plot_wind(dates, wind_speeds)

        return render_template('weather.html',
                               plot_url_temp=plot_url_temp,
                                 plot_url_wind=plot_url_wind,
                               start_warning=start_warning,
                               start_weather=start_weather_info,
                               start_hourly_weather=start_hourly_weather_data.list,
                               end_warning=end_warning,
                               end_weather=end_weather_info,
                               end_hourly_weather=end_hourly_weather_data.list)

    except Exception as e:
        current_app.logger.error(f"Error in weather route: {e}")
        return render_template('weather.html',
                               error=_("Unable to fetch weather data"))
