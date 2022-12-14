from sqlalchemy.exc import OperationalError
from dotenv import load_dotenv
from models import *
from json import load, dump
from pathlib import Path
from sqlalchemy import create_engine, MetaData
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import logging

FORMAT = "%(asctime)s - %(levelname)s" \
             "- %(funcName)s: %(lineno)d - %(message)s"
logging.basicConfig(format=FORMAT, level=logging.DEBUG)


class DbManager:
    def __init__(
            self, user: str, password: str,
            host: str, db_name: str, api_key: str
    ):
        self.user = user
        self.password = password
        self.host = host
        self.db_name = db_name
        self.api_key = api_key

    def create_db(self):
        try:
            connection = psycopg2.connect(user=self.user, password=self.password)
            connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            with connection.cursor() as cursor:
                cursor.execute(f'create database {self.db_name}')
        except psycopg2.errors.DuplicateDatabase as e1:
            logging.error(e1)
        except psycopg2.OperationalError as e2:
            logging.error(e2)
        else:
            logging.debug(f'Database {self.db} is created')
            connection.close()

    def create_engine(self):
        try:
            engine = create_engine(f'postgresql+psycopg2://{self.user}:{self.password}@{self.host}/{self.db_name}')
            engine.connect()
            logging.debug('Engine created')
        except OperationalError as e:
            logging.error(e)
        else:
            return engine

    def create_tables(self, base):
        engine = self.create_engine()
        if engine:
            base.metadata.create_all(engine)
            logging.debug('Tables created')

    def drop_tables(self, base):
        engine = self.create_engine()
        if engine:
            base.metadata.drop_all(engine)
            logging.debug('All tables deleted')


def get_path(file_name):
    cur_path = Path(__file__).parents[1]
    new_path = Path(cur_path, 'data', file_name)
    return new_path


