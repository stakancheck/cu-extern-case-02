from flask import Flask, request
from flask_babel import Babel

app = Flask(__name__)
babel = Babel(app)

@babel.localeselector
def get_locale():
    # Здесь логика определения языка
    return request.accept_languages.best_match(['en', 'ru'])
