from datetime import datetime
import pytz


class Contact(object):
    def __init__(self,
                 database_id: int,
                 first_name: str,
                 phone_number: str,
                 last_name: str = None,
                 created_time: datetime = datetime.now(tz=pytz.timezone('Asia/Tehran')),
                 ):
        self.database_id = database_id
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.created_time = created_time

    @property
    def database_id(self) -> int:
        return self.__database_id

    @property
    def first_name(self) -> str:
        return self.__first_name

    @property
    def last_name(self) -> str:
        return self.__last_name

    @property
    def phone_number(self) -> str:
        return self.__phone_number

    @property
    def created_time(self) -> datetime:
        return self.__created_time

    @database_id.setter
    def database_id(self, database_id: int) -> None:
        self.__database_id = database_id

    @staticmethod
    def __check_name(name: str):
        if not name.replace(' ', '').isalpha():
            raise ValueError("all characters must only contain alphanumeric characters")
        elif len(name) > 30:
            raise ValueError("name is too long")

    @first_name.setter
    def first_name(self, first_name: str) -> None:
        if not first_name or not first_name.strip():
            raise ValueError("first name cannot be empty or None")
        self.__check_name(first_name)
        self.__first_name = first_name

    @last_name.setter
    def last_name(self, last_name: str) -> None:
        if not last_name or not last_name.strip():
            self.__last_name = None
        else:
            self.__check_name(last_name)
            self.__last_name = last_name

    @staticmethod
    def __check_number(number: str):
        if not number.isdecimal():
            raise ValueError("number must only contain decimal numbers")
        elif len(number) > 11:
            raise ValueError("number is too long")

    @phone_number.setter
    def phone_number(self, phone_number: str) -> None:
        if not phone_number or not phone_number.strip():
            raise ValueError("phone number cannot be empty or None")
        self.__check_number(phone_number)
        self.__phone_number = phone_number

    @created_time.setter
    def created_time(self, created_time: datetime) -> None:
        created_time = created_time.astimezone(tz=pytz.timezone('Asia/Tehran'))
        self.__created_time = created_time
