class BaseCustomException(Exception):
    message: str = ''

    def __init__(self, *args, msg: str = '') -> None:
        self.message = msg or self.message
        super().__init__(*args)

    def __str__(self) -> str:
        return self.message


class CityNameError(BaseCustomException):
    message = "Can't set data from api. Check city_name is correct."


class ApiKeyError(BaseCustomException):
    message = "Can't get data from api. Check api_key is correct."


class EmptyFileError(BaseCustomException):
    message = 'File is empty. Please fill the data.'


class JsonWrongStructure(BaseCustomException):
    message = 'JSON file has wrong structure. ' \
              'Rebuild data structure to JSON format.'
