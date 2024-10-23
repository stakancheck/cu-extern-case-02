from dotenv import load_dotenv
import os


load_dotenv()

class Config:
    OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')
    BABEL_DEFAULT_LOCALE = 'ru'
    BABEL_TRANSLATION_DIRECTORIES = 'app/translations'
