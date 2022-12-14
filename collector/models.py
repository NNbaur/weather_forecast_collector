from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class Cities(Base):
    __tablename__ = 'cities'
    id = Column(Integer(), primary_key=True)
    city_name = Column(String(30), nullable=False)
    latitude = Column(Float())
    longitude = Column(Float())
    country = Column(String(30))

    def __repr__(self):
        return f"Cities(" \
               f"id={self.id!r}," \
               f"city_name={self.city_name!r}," \
               f"latitude={self.latitude!r}," \
               f"longitude={self.longitude!r}," \
               f"country={self.country!r})"


class WeatherCommon(Base):
    __tablename__ = 'weather_common'
    id = Column(Integer(), primary_key=True)
    city_id = Column(ForeignKey('cities.id'), nullable=False)
    created_at = Column(DateTime(), default=datetime.now())
    weather = Column(String(30))
    description = Column(String(50))

    def __repr__(self):
        return f"WeatherCommon(" \
               f"id={self.id!r}," \
               f"city_id={self.city_id!r}," \
               f"created_at={self.created_at!r}," \
               f"weather={self.weather!r}," \
               f"description={self.description!r})"


class WeatherMain(Base):
    __tablename__ = 'weather_main'
    id = Column(Integer(), primary_key=True)
    weather_common_id = Column(ForeignKey('weather_common.id'), nullable=False)
    temperature = Column(Float())
    feels_like = Column(Float())
    temp_min = Column(Float())
    temp_max = Column(Float())
    pressure = Column(Integer())
    humidity = Column(Integer())

    def __repr__(self):
        return f"WeatherMain(" \
               f"id={self.id!r}," \
               f"weather_common_id={self.weather_common_id!r}," \
               f"temperature={self.temperature!r}," \
               f"feels_like={self.feels_like!r}," \
               f"temp_min={self.temp_min!r}," \
               f"temp_max ={self.temp_max!r}," \
               f"pressure={self.pressure!r}," \
               f"humidity={self.humidity!r})"


class WeatherSecond(Base):
    __tablename__ = 'weather_second'
    id = Column(Integer(), primary_key=True)
    weather_common_id = Column(ForeignKey('weather_common.id'), nullable=False)
    visibility = Column(Integer())
    wind_speed = Column(Float())
    wind_deg = Column(Float())
    clouds = Column(Integer())

    def __repr__(self):
        return f"WeatherSecond(" \
               f"id={self.id!r}," \
               f"weather_common_id={self.weather_common_id!r}," \
               f"visibility={self.visibility!r}," \
               f"wind_speed={self.wind_speed!r}," \
               f"wind_deg={self.wind_deg!r}," \
               f"clouds={self.clouds!r})"
