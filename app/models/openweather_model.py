from datetime import datetime, timedelta

from pydantic import BaseModel, Field
from typing import List, Optional

class Coord(BaseModel):
    lon: float
    lat: float

class Weather(BaseModel):
    id: int
    main: str
    description: str
    icon: str

class Main(BaseModel):
    temp: float
    feels_like: float
    pressure: int
    humidity: int
    temp_min: Optional[float] = None
    temp_max: Optional[float] = None
    sea_level: Optional[int] = None
    grnd_level: Optional[int] = None

    @property
    def rounded_temp(self) -> int:
        return int(round(self.temp))

class Wind(BaseModel):
    speed: float
    deg: Optional[int] = None
    gust: Optional[float] = None

class Clouds(BaseModel):
    all: int

class Rain(BaseModel):
    one_h: Optional[float] = Field(None, alias='1h')

class Snow(BaseModel):
    one_h: Optional[float] = Field(None, alias='1h')

class OpenWeatherResponse(BaseModel):
    coord: Optional[Coord] = None
    weather: Optional[List[Weather]] = None
    base: Optional[str] = None
    main: Main
    visibility: Optional[int] = None
    wind: Wind
    clouds: Optional[Clouds] = None
    rain: Optional[Rain] = None
    snow: Optional[Snow] = None
    dt: Optional[int] = None
    timezone: Optional[int] = None
    id: Optional[int] = None
    name: Optional[str] = None
    cod: Optional[int] = None

    @property
    def pretty_dt(self) -> str | None:
        if self.dt:
            local_time = datetime.fromtimestamp(self.dt)
            return local_time.strftime('%d.%m %H:%M')
        return None

class City(BaseModel):
    id: int
    name: str
    coord: Coord
    country: str
    population: int
    timezone: int
    sunrise: int
    sunset: int

class OpenWeatherHourlyResponse(BaseModel):
    cod: str
    message: Optional[int] = None
    cnt: Optional[int] = None
    list: Optional[List[OpenWeatherResponse]] = None
    city: Optional[City] = None
