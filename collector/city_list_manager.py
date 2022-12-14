import json
from json import load, dump
import logging
from os.path import exists
from pathlib import Path
from os import stat

FORMAT = "%(asctime)s - %(levelname)s" \
             "- %(funcName)s: %(lineno)d - %(message)s"
logging.basicConfig(format=FORMAT, level=logging.DEBUG)

class MyException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg

# class CityListConfigCheck:
#     def __init__(self, path: str):
#         self.path = path
#
#     def _check_file_exist(self) -> bool:
#         check = Path(self.path).exists()
#         if not check:
#             logging.error('File does not exist')
#         return check
#
#     def _check_file_extension(self) -> bool:
#         check = Path(self.path).suffix == '.json'
#         if not check:
#             logging.error('File is not JSON. Please use JSON file')
#         return check
#
#     def _check_file_empty(self) -> bool:
#         check = Path(self.path).stat().st_size != 0
#         if not check:
#             logging.error('File is empty. Fill the file with data')
#         return check
#
#     def _check_file_json_structure(self) -> bool:
#         try:
#             json.load(open(self.path))
#         except json.decoder.JSONDecodeError:
#             logging.error('JSON decoding error. Check the structure of JSON')
#             return False
#         return True
#
#     def check_config_file(self) -> bool:
#         check1 = self._check_file_exist()
#         if check1:
#             check2 = self._check_file_extension()
#             check3 = self._check_file_empty()
#             if check2 and check3:
#                 check4 = self._check_file_json_structure()
#                 return all([check1, check2, check3, check4])
#         return False


class CityList:
    def __init__(self, path: str):
        self.path = path
        self.check = self._check_config_file()

    def _check_config_file(self) -> bool:
        try:
            with open(self.path, 'r+') as f:
                load(f)
        except json.decoder.JSONDecodeError as e:
            logging.error(f'File is empty or json structure is wrong. Details: {e}')
            return False
        except FileNotFoundError:
            logging.error('File does not exist')
            return False
        return True

    def get_city_list(self) -> list | None:
        if self.check:
            with open(self.path, 'r') as f:
                s = load(f)
            return s

    def add_city_in_list(self, city: str):
        if self.check:
            with open(self.path, 'r+') as f:
                data = load(f)
                city = {"name": city}
                if city not in data:
                    data.append(city)
                    f.seek(0)
                    f.truncate()
                    dump(data, f, indent=4)
                    logging.debug(f'{city["name"]} added in list')
                else:
                    logging.debug(f'{city["name"]} already in list')

    def delete_city_from_list(self, city: str):
        if self.check:
            with open(self.path, 'r+') as f:
                data = load(f)
                city = {"name": city}
                if city in data:
                    ind = data.index(city)
                    deleted_city = data.pop(ind)
                    f.seek(0)
                    f.truncate()
                    dump(data, f, indent=4)
                    logging.debug(f'City {deleted_city["name"]} is removed from city_list')
                else:
                    logging.debug('City is not in list. Check the name of the city is correct')


city = CityList('../data/city_list2.json')
a = city._check_config_file()
b = city.check
print(a, b)
#city.delete_city_from_list('Astana')