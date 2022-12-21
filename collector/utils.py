from datetime import datetime, timedelta
from pathlib import Path
from json import load
from typing import List, Callable
import logging
import json
from collector.exceptions import EmptyFileError, JsonWrongStructure
import os
from apscheduler.schedulers.blocking import BlockingScheduler


def get_local_time(timezone: int) -> datetime | None:
    if isinstance(timezone, int):
        td: timedelta = timedelta(seconds=timezone)
        utc_now: datetime = datetime.utcnow()
        local_time: datetime = utc_now + td
        return local_time
    return None


def get_path(dir_name: str = 'data', file: str = 'city_list.json') -> Path:
    if isinstance(dir_name, str) and isinstance(file, str):
        cur_path: Path = Path(__file__).parents[1]
        new_path: Path = Path(cur_path, dir_name, file)
        return new_path
    return None


def get_city_list(path: Path | str) -> List[dict] | None:
    if isinstance(path, Path) or isinstance(path, str):
        try:
            with open(path, 'r+') as f:
                city_list = load(f)
        except json.decoder.JSONDecodeError:
            if os.path.getsize(path) == 0:
                logging.error('File is empty. Please fill the data.')
                raise EmptyFileError
            logging.error(
                'JSON file has wrong structure. '
                'Rebuild data structure to JSON format.'
            )
            raise JsonWrongStructure
        except FileNotFoundError:
            logging.error('File does not exist')
            raise FileNotFoundError('File does not exist')
        else:
            return city_list
    return None


def start_scheduler(job: Callable) -> None:
    scheduler = BlockingScheduler()
    scheduler.add_job(job, 'interval', seconds=1)
    scheduler.start()
