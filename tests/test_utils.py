import time
from datetime import datetime
import pytest
from collector.utils import get_local_time, get_path, get_city_list, start_scheduler
from pathlib import Path
from freezegun import freeze_time
from collector.exceptions import JsonWrongStructure, EmptyFileError


@freeze_time("2022-12-20 17:55:0")
def test_local_time():
    assert get_local_time(3600) == datetime(2022, 12, 20, 18, 55, 0)
    assert get_local_time(0) == datetime(2022, 12, 20, 17, 55, 0)
    assert get_local_time(-3600) == datetime(2022, 12, 20, 16, 55, 0)
    assert get_local_time(86400) == datetime(2022, 12, 21, 17, 55, 0)
    assert get_local_time('3600') is None


def test_get_path():
    assert get_path() == Path(
        Path(__file__).parents[1],
        'data',
        'city_list.json'
    )
    assert get_path('dirs', 'file2.txt') == Path(
        Path(__file__).parents[1],
        'dirs',
        'file2.txt'
    )
    assert get_path('', '') == Path(Path(__file__).parents[1])
    assert get_path(24, 24) is None


def test_get_city_list():
    with pytest.raises(EmptyFileError) as e1:
        get_city_list('tests/fixtures/utils_fixtures/city_list1.txt')
    assert str(e1.value) == 'File is empty. Please fill the data.'
    with pytest.raises(JsonWrongStructure) as e2:
        get_city_list('tests/fixtures/utils_fixtures/city_list2.json')
    assert str(e2.value) == 'JSON file has wrong structure. ' \
                            'Rebuild data structure to JSON format.'
    with pytest.raises(FileNotFoundError) as e3:
        get_city_list('tests/fixtures/utils_fixtures/city_list3.json')
        get_city_list('')
    assert str(e3.value) == "File does not exist"

    city_list1 = get_city_list('tests/fixtures/utils_fixtures/city_list4.json')
    assert city_list1 == [{"name": "Almaty"}, {"name": "Astana"}]

    city_list2 = get_city_list(55)
    assert city_list2 is None



