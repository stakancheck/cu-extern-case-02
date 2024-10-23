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
    temp_min: float
    temp_max: float
    sea_level: Optional[int] = None
    grnd_level: Optional[int] = None

class Wind(BaseModel):
    speed: float
    deg: int
    gust: Optional[float] = None

class Clouds(BaseModel):
    all: int

class Rain(BaseModel):
    one_h: Optional[float] = Field(None, alias='1h')

class Snow(BaseModel):
    one_h: Optional[float] = Field(None, alias='1h')

class Sys(BaseModel):
    type: Optional[int] = None
    id: Optional[int] = None
    message: Optional[float] = None
    country: str
    sunrise: int
    sunset: int

class OpenWeatherResponse(BaseModel):
    coord: Coord
    weather: List[Weather]
    base: str
    main: Main
    visibility: Optional[int] = None
    wind: Wind
    clouds: Clouds
    rain: Optional[Rain] = None
    snow: Optional[Snow] = None
    dt: int
    sys: Sys
    timezone: int
    id: int
    name: str
    cod: int
