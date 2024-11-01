import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler

from flask import Flask, request, session
from flask_babel import Babel

from config import Config
from .routes import weather_bp


def create_app():
    app = Flask(__name__)

    # @app.template_filter('datetimeformat')
    # def datetimeformat(value, format='%Y-%m-%d'):
    #     return datetime.fromtimestamp(value).strftime(format)

    # Загрузка конфигурации
    app.config.from_object(Config)
    Config.init_app(app)

    # Настройка логирования
    if not app.debug and not app.testing:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler(
            'logs/weather_app.log',
            maxBytes=10240,
            backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.DEBUG)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.DEBUG)
        app.logger.info('Weather app startup')

    def get_locale():
        lang = request.args.get('lang')
        if lang:
            return lang
        if 'language' in session:
            return session['language']
        return request.accept_languages.best_match(app.config['LANGUAGES'])

    Babel(app, locale_selector=get_locale)

    app.register_blueprint(weather_bp)

    return app
