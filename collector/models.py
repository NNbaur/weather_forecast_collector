from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy.orm import relationship
from typing import TypeAlias

Base: TypeAlias = declarative_base()  # type: ignore


# Table Cities for database, to store list of cities
class Cities(Base):
    __tablename__ = 'cities'
    id = Column(Integer, primary_key=True)
    city_name = Column(String(30), nullable=False, unique=True)
    latitude = Column(Float)
    longitude = Column(Float)
    country = Column(String(30))
    weather_data = relationship(
        'Weather',
        backref='cities',
        cascade='all, delete-orphan'
    )

    def __repr__(self):
        return f'Cities(' \
               f'id={self.id!r},' \
               f'city_name={self.city_name!r},' \
               f'latitude={self.latitude!r},' \
               f'longitude={self.longitude!r},' \
               f'country={self.country!r})'


# Table Weather to database, to store cities weather data
class Weather(Base):
    __tablename__ = 'weather'
    id = Column(Integer, primary_key=True)
    city_id = Column(
        Integer,
        ForeignKey('cities.id'),
        nullable=False
    )
    created_at = Column(
        DateTime,
        default=datetime.now(),
        comment='Date and time of server, when data collected.'
    )
    local_time = Column(
        DateTime,
        comment='Local time of the city, in the moment of weather collected.'
    )
    weather = Column(
        String(30),
        comment='The weather in the city.'
    )
    description = Column(
        String(50),
        comment='Short description of the weather.'
    )
    temperature = Column(
        Float,
        comment='Current average temperature in the city. Celsius.'
    )
    feels_like = Column(
        Float,
        comment='This temperature parameter accounts'
                'for the human perception of weather. Celsius.'
    )
    temp_min = Column(
        Float,
        comment='Minimum temperature at the moment of calculation.'
                'This is minimal currently observed temperature'
                '(within large megalopolises and urban areas). Celsius.'
    )
    temp_max = Column(
        Float,
        comment='Maximum temperature at the moment of calculation.'
                'This is maximal currently observed temperature'
                '(within large megalopolises and urban areas). Celsius.'
    )
    pressure = Column(
        Integer,
        comment='Atmospheric pressure. hPa.'
    )
    humidity = Column(
        Integer,
        comment='Humidity. %.'
    )

    def __repr__(self):
        return f'Weather(' \
               f'id={self.id!r},' \
               f'city_id={self.city_id!r},' \
               f'created_at={self.created_at!r},' \
               f'local_time={self.local_time!r},' \
               f'weather={self.weather!r},' \
               f'description={self.description!r},' \
               f'temperature={self.temperature!r},' \
               f'feels_like={self.feels_like!r},' \
               f'temp_min={self.temp_min!r},' \
               f'temp_max ={self.temp_max!r},' \
               f'pressure={self.pressure!r},' \
               f'humidity={self.humidity!r})'
