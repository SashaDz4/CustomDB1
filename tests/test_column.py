import datetime
from typing import Type

import interval
import pytest

from models.column import Column, IntCol, RealCol, CharCol, StringCol, TimeCol, TimeIntervalCol


def test_column_default_validation():
    class TestColumn(Column):
        @staticmethod
        def validate(value):
            return value == "correct"

    col = TestColumn("test_type", "test_name", "correct")
    assert col.default == "correct"

    with pytest.raises(TypeError) as exception_info:
        TestColumn("test_type", "test_name", "incorrect")

    assert exception_info.value.args[0] == (
        "This value 'incorrect' does not pass column validation! Column 'test_name' has "
        "type 'test_type' and entered type is 'str'"
    )


def test_int_col_validation():
    col = IntCol("amount")
    assert col.validate(10)
    assert not col.validate("asdf")


def test_float_col_validation():
    col = RealCol("price")
    assert col.validate(10.0)
    assert not col.validate(10)


def test_char_col_validation():
    col = CharCol("class")
    assert col.validate("A")
    assert not col.validate("BCD")


def test_string_col_validation():
    col = StringCol("name")
    assert col.validate("John Snow")
    assert not col.validate(True)


def test_time_col_validation():
    col = TimeCol("name")
    assert col.validate(datetime.time(12, 23, 34))
    assert not col.validate("12:34:56")


def test_time_interval_col_validation():
    col = TimeIntervalCol("name")
    assert col.validate(interval.Interval(datetime.time(12, 23, 34),
                                          datetime.time(12, 23, 35)))
    assert not col.validate("12:34:56:78 - 12:34:56:79")