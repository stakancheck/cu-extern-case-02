import logging
import os
from typing import Any, Dict
from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

from app.services.weather_service import WeatherService
from app.services.weather_analyzer_service import WeatherAnalyzerService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

# Bot token
API_TOKEN = os.getenv('TG_BOT_TOKEN')

# Initialize router
router = Router()


class WeatherForm(StatesGroup):
    start_city = State()
    end_city = State()


@router.message(CommandStart())
async def send_welcome(message: Message) -> None:
    await message.reply(
        "Привет! Я бот для предсказания неблагоприятных погодных условий. "
        "Используй команду /weather, чтобы узнать погоду для маршрута."
    )


@router.message(Command("help"))
async def send_help(message: Message) -> None:
    await message.reply(
        "/start - Приветственное сообщение\n"
        "/help - Список доступных команд\n"
        "/weather - Узнать погоду для маршрута"
    )


@router.message(Command("weather"))
async def weather_start(message: Message, state: FSMContext) -> None:
    await state.set_state(WeatherForm.start_city)
    await message.reply("Введите начальную точку маршрута:")


@router.message(WeatherForm.start_city)
async def process_start_city(message: Message, state: FSMContext) -> None:
    await state.update_data(start_city=message.text)
    await state.set_state(WeatherForm.end_city)
    await message.reply("Введите конечную точку маршрута:")


@router.message(WeatherForm.end_city)
async def process_end_city(message: Message, state: FSMContext) -> None:
    await state.update_data(end_city=message.text)
    data = await state.get_data()

    start_city = data['start_city']
    end_city = data['end_city']

    try:
        weather_service = WeatherService()
        analyzer = WeatherAnalyzerService()

        start_weather = weather_service.get_weather_by_city(start_city)
        end_weather = weather_service.get_weather_by_city(end_city)

        start_warning = analyzer.analyze_weather(start_weather)
        end_warning = analyzer.analyze_weather(end_weather)

        response = (
            f"Погода в {start_city}:\n"
            f"Температура: {start_weather.main.temp}°C\n"
            f"Описание: {start_weather.weather[0].description}\n"
            f"Предупреждение: {start_warning.description}\n\n"
            f"Погода в {end_city}:\n"
            f"Температура: {end_weather.main.temp}°C\n"
            f"Описание: {end_weather.weather[0].description}\n"
            f"Предупреждение: {end_warning.description}"
        )

        await message.reply(response)
    except Exception as e:
        logger.error(f"Error fetching weather data: {e}")
        await message.reply(
            "Произошла ошибка при получении данных о погоде. "
            "Пожалуйста, попробуйте снова."
        )

    await state.clear()


async def main() -> None:
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    # Register router
    dp.include_router(router)

    # Start polling
    await dp.start_polling(bot)


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
