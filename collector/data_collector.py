from utils import get_path, get_city_list, start_scheduler
from db_manager import DbManager, Collector


def initial_run() -> None:
    # 1) Get path to city_list.json
    path1 = get_path()
    # 2) Get city_list in json format
    city_list = get_city_list(path1)
    # 3) If city_list file correct run configurations
    # 3.1) Create DbManager object to interaction with database
    # Default name of db is weather_collector, if you need
    # another name, enter the db_name in DbManager: DbManager(db_name='custom')
    # Default address of db 'localhost';
    # username and password get from .env by default
    db_manager = DbManager()
    # 3.2) Create individual db for weather forecast
    db_manager.create_db()
    # 3.3) Create tables in db
    db_manager.create_tables()
    # 3.4) Insert data to tables
    collector = Collector(city_list)
    collector.insert_data_to_table('cities')
    collector.insert_data_to_table('weather')


def collect_weather() -> None:
    # Get city_list data
    path1 = get_path()
    city_list = get_city_list(path1)
    # Collect data from api to db
    collector = Collector(city_list)
    collector.insert_data_to_table('weather')


if __name__ == '__main__':
    initial_run()
    start_scheduler(collect_weather)

