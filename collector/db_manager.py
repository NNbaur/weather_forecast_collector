import logging
import requests
from os import getenv
import psycopg2 as pc2
from typing import List
from dotenv import load_dotenv
from sqlalchemy.engine.base import Engine
from utils import get_local_time, get_path
from sqlalchemy.orm import Session
from models import Cities, Weather, Base as base
from exceptions import CityNameError, ApiKeyError
from sqlalchemy.orm.exc import UnmappedInstanceError
from sqlalchemy import create_engine, select, inspect
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy.exc import OperationalError, IntegrityError, ProgrammingError


load_dotenv()
api_key = getenv('API_KEY')
user = getenv('USER')
password = getenv('PASS')

p = get_path(dir_name='', file='file.log')
FORMAT = "%(asctime)s - %(levelname)s" \
             "- %(funcName)s: %(lineno)d - %(message)s"
logging.basicConfig(format=FORMAT, level=logging.DEBUG, filename=p)


class DbManager:
    """
    DbManager provides to interact with database.

    Attributes:
        user: username of database user. Defaults to user from .env.
        password: password of database user. Defaults to password from .env.
        host: address of database. Defaults to 'localhost'.
        db_name: name of database. Defaults to 'weather_collector'.
    """

    def __init__(
            self, user: str | None = user, password: str | None = password,
            host: str = 'localhost', db_name: str = 'weather_collector'
    ) -> None:
        self.user = user
        self.password = password
        self.host = host
        self.db_name = db_name

    def create_db(self) -> None:
        """
        Create database with name from class attributes - db_name
        """
        # Connect to postgresql with psycopg2
        try:
            connection = pc2.connect(
                user=self.user,
                password=self.password
            )
            connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            with connection.cursor() as cursor:
                # Make sql request to create database
                cursor.execute(f'create database {self.db_name}')
        # Handle exceptions, if database already exist
        # or take wrong user/password
        except (pc2.errors.DuplicateDatabase, pc2.OperationalError) as err:
            logging.error(err)
        else:
            logging.debug(f'Database {self.db_name} is created')
            connection.close()

    def create_engine(self) -> Engine | None:
        """
        Create new class instance from sqlalchemy.engine,
        that provides connection to database
        """
        try:
            engine = create_engine(
                f'postgresql+psycopg2://{self.user}:{self.password}@{self.host}/{self.db_name}'
            )
            engine.connect()
        # Handle exception if data for create_engine is incorrect:
        # username, password, address or db_name
        except OperationalError as err:
            logging.error(err)
        else:
            logging.debug('Engine created')
            return engine
        return None

    def create_tables(self) -> None:
        """
        Create all tables in database.
        Tables and their structures located in models.py.
        """
        engine = self.create_engine()
        if engine:
            base.metadata.create_all(engine)
            logging.debug('Tables created')
        else:
            logging.debug('Tables not created. Check engine.')

    def drop_tables(self) -> None:
        """
        Delete all tables from database.
        Tables and their structures located in models.py.
        """
        engine = self.create_engine()
        if engine:
            base.metadata.drop_all(engine)
            logging.debug('All tables deleted')
        else:
            logging.debug('Tables not deleted. Check engine.')

    def truncate_table(self, table: str) -> None:
        """
        Delete a table and all related tables.
        """
        engine = self.create_engine()
        session = Session(engine)
        try:
            session.execute(f'TRUNCATE {table} CASCADE')
        except ProgrammingError as err:
            logging.error(err)
            session.rollback()
        else:
            logging.debug(
                f'Table {table} and all related tables deleted from database'
            )
            session.commit()

    def get_weather_list(self) -> list:
        engine = self.create_engine()
        session = Session(engine)
        res = session.query(
            Weather.id, Cities.city_name, Weather.created_at,
            Weather.local_time, Weather.weather, Weather.description,
            Weather.temperature, Weather.feels_like, Weather.temp_min,
            Weather.temp_max, Weather.pressure, Weather.humidity
        ).join(Cities).all()
        return res

    def get_city_list(self) -> list:
        engine = self.create_engine()
        session = Session(engine)
        res = session.query(Cities).all()
        return res


class Collector(DbManager):
    """
    Collector provides to collect data of weather in different cities
    with API(OpenWeatherAPI) and store it to database
    Collector is inherited from DbManager
    and has all functionality as DbManager.

    Attributes:
        user: username of database user. Defaults to user from .env.
        password: password of database user. Defaults to password from .env.
        host: address of database. Defaults to 'localhost'.
        db_name: name of database. Defaults to 'weather_collector'.
        city_list: list of cities.
        api: api key for connection to api service.
    """
    def __init__(
            self, city_list: List[dict] | None, user: str | None = user,
            password: str | None = password, host: str = 'localhost',
            db_name: str = 'weather_collector', api: str | None = api_key
    ) -> None:
        super().__init__(user, password, host, db_name)
        self.city_list = city_list
        self.api = api

    def get_request_from_api(self, city: dict) -> dict | None:
        """
        Make request to api for a specific city.
        :returns: response in json format or raise exception
        """
        req = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?'
            f'q={city["name"]}&units=metric&appid={self.api}'
        ).json()
        match str(req['cod']):
            case '200':
                return req
            case '404':
                raise CityNameError
            case '401':
                raise ApiKeyError
        return None

    def insert_data_to_table(self, table: str) -> None:
        """
        Insert collected weather data to database
        """
        engine = self.create_engine()
        session = Session(engine)

        if not inspect(engine).has_table(table):
            logging.debug(f'Table {table} is not exist')
            return None

        if not self.city_list:
            return None

        for city in self.city_list:
            try:
                req = self.get_request_from_api(city)
                data_insert = self.get_insert_request_to_db(table, city, req)
                session.add(data_insert)
            except (
                    CityNameError,
                    ApiKeyError,
                    UnmappedInstanceError,
                    IntegrityError
            ) as err:
                logging.error(err)
                session.rollback()
                break

        if session.new:
            logging.debug(f'Data inserted to table {table}')
            session.commit()

    def get_insert_request_to_db(
            self, table: str, city: dict, req: dict | None
    ) -> object | None:
        if req:
            tables = {
                "cities": Cities(
                    city_name=city["name"],
                    latitude=req['coord']['lat'],
                    longitude=req['coord']['lon'],
                    country=req['sys']['country']),
                "weather": Weather(
                    city_id=select(Cities.id).where(
                        Cities.city_name == city["name"]
                    ).scalar_subquery(),
                    local_time=get_local_time(req['timezone']),
                    weather=req['weather'][0]['main'],
                    description=req['weather'][0]['description'],
                    temperature=req['main']['temp'],
                    feels_like=req['main']['feels_like'],
                    temp_min=req['main']['temp_min'],
                    temp_max=req['main']['temp_max'],
                    pressure=req['main']['pressure'],
                    humidity=req['main']['humidity'],)
            }
            try:
                insert_req = tables[table]
            except KeyError:
                logging.error(
                    f'Data not inserted to table {table}.'
                    f'{table} is not exists'
                )
                return None
            else:
                return insert_req
        logging.debug("Request to API didn't created.")
        return None
