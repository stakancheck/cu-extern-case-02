from datetime import timedelta

from dotenv import load_dotenv
import os


load_dotenv()

class Config:
    BABEL_DEFAULT_LOCALE = 'ru'
    LANGUAGES = ['ru', 'en']

    # OpenWeather настройки
    OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')

    # Настройки безопасности
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = timedelta(days=1)

    DEBUG = False
    TESTING = False

    @classmethod
    def init_app(cls, app):
        pass
