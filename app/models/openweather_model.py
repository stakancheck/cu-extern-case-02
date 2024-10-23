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

class Sys(BaseModel):
    type: Optional[int] = None
    id: Optional[int] = None
    message: Optional[float] = None
    country: str
    sunrise: int
    sunset: int

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
    sys: Optional[Sys] = None
    timezone: Optional[int] = None
    id: Optional[int] = None
    name: Optional[str] = None
    cod: Optional[int] = None
