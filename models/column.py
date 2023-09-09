from datetime import time

from Pyro5.api import expose
from abc import ABC, abstractmethod
import re
from dataclasses import dataclass
from typing import Any
from datetime import datetime
from interval import Interval


COLUMN_TYPE_CHOICES = ["int", "real", "char", "string", "time", "time interval"]


@expose
@dataclass
class Column(ABC):
    _type: str
    _name: str
    default: Any

    def __post_init__(self) -> None:
        self.validate_or_error(self.default)

    @property
    def name(self):
        return self._name

    @property
    def type(self):
        return self._type

    @staticmethod
    @abstractmethod
    def validate(value) -> bool:
        pass

    def validate_or_error(self, value: Any) -> None:
        if not self.validate(value):
            raise TypeError(
                f"This value '{value}' does not pass column validation! "
                f"Column '{self.name}' has type '{self.type}' and entered type is "
                f"'{type(value).__name__}'"
            )


@expose
class IntCol(Column):
    TYPE = "int"
    DEFAULT = 0

    def __init__(self, name: str, default: int = DEFAULT) -> None:
        super().__init__(IntCol.TYPE, name, default)

    @staticmethod
    def validate(value) -> bool:
        return isinstance(value, int)


@expose
class RealCol(Column):
    TYPE = "real"
    DEFAULT = 0.0

    def __init__(self, name: str, default: float = DEFAULT) -> None:
        super().__init__(RealCol.TYPE, name, default)

    @staticmethod
    def validate(value) -> bool:
        return isinstance(value, float)


@expose
class CharCol(Column):
    TYPE = "char"
    DEFAULT = "_"

    def __init__(self, name: str, default: str = DEFAULT) -> None:
        super().__init__(CharCol.TYPE, name, default)

    @staticmethod
    def validate(value) -> bool:
        return isinstance(value, str) and len(value) == 1


@expose
class StringCol(Column):
    TYPE = "string"
    DEFAULT = ""

    def __init__(self, name: str, default: str = DEFAULT) -> None:
        super().__init__(StringCol.TYPE, name, default)

    @staticmethod
    def validate(value) -> bool:
        return isinstance(value, str)


@expose
class TimeCol(Column):
    TYPE = "time"
    FORMAT = "%H:%M:%S"
    DEFAULT = datetime.strptime("00:00:00", FORMAT).time()

    def __init__(self, name: str, default: str = DEFAULT) -> None:
        super().__init__(TimeCol.TYPE, name, default)

    @staticmethod
    def validate(value) -> bool:
        return isinstance(value, time)


@expose
class TimeIntervalCol(Column):
    TYPE = "time interval"
    DEFAULT = Interval(
        datetime.strptime("00:00:00", TimeCol.FORMAT).time(),
        datetime.strptime("12:00:00", TimeCol.FORMAT).time()
    )

    def __init__(self, name: str, default: str = DEFAULT) -> None:
        super().__init__(TimeIntervalCol.TYPE, name, default)

    @staticmethod
    def validate(value) -> bool:
        return isinstance(value, Interval)