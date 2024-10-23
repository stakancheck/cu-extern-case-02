# app/__init__.py
from flask import Flask, request, session
from flask_babel import Babel


def create_app():
    app = Flask(__name__)

    # Инициализация Babel
    babel = Babel(app)

    # Настройка локали
    @babel.localeselector
    def get_locale():
        lang = request.args.get('lang')
        if lang:
            return lang

        if 'language' in session:
            return session['language']

        return request.accept_languages.best_match(['en', 'ru'])

    return app
