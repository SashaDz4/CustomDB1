import datetime

import pytest

from models.column import IntCol, StringCol, CharCol, TimeCol, TimeIntervalCol
from models.table import Table


def test_add_column():
    table = Table("test")

    assert table.columns_count == 0

    test_col = IntCol("amount")

    table.add_column(test_col)

    assert table.columns_count == 1

    with pytest.raises(ValueError) as exception_info:
        table.add_column(test_col)

    assert (
        exception_info.value.args[0]
        == "Column with name 'amount' already exists in the table!"
    )


def test_add_row():
    table = Table("test")

    assert table.rows_count == 0

    with pytest.raises(ValueError) as exception_info:
        table.add_row({})

    assert exception_info.value.args[0] == "Row data cannot be empty!"

    with pytest.raises(ValueError) as exception_info:
        table.add_row({"amount": 1})

    assert (
        exception_info.value.args[0]
        == "Invalid column names: ('amount',) is not subset of ()!"
    )

    table.add_column(IntCol("amount"))
    table.add_row({"amount": 10})
    assert table.get_row(0).values == [10]

    with pytest.raises(TypeError):
        table.add_row({"amount": "hello"})


def test_add_column_after_add_row():
    table = Table("test")
    table.add_column(IntCol("amount"))
    table.add_row({"amount": 1})

    assert table.rows_count == 1
    assert table.get_row(0).values == [1]

    table.add_column(TimeCol("time"))
    table.add_row({"amount": 2, "time": datetime.time(12, 23, 34)})

    assert table.rows_count == 2
    assert table.get_row(0).values == [1, datetime.time(00, 00, 00)]
    assert table.get_row(1).values == [2, datetime.time(12, 23, 34)]


def test_table_str():
    table = Table("test")
    assert str(table) == "Table: test\n"

    table.add_column(IntCol("amount"))
    assert (
        str(table)
        == """Table: test
+--------------+---------------+
| index: int   | amount: int   |
+==============+===============+
+--------------+---------------+"""
    )

    table.add_column(TimeCol("time"))
    assert (
        str(table)
        == """Table: test
+--------------+---------------+--------------+
| index: int   | amount: int   | time: time   |
+==============+===============+==============+
+--------------+---------------+--------------+"""
    )

    table.add_row({"amount": 10, "time": datetime.time(12, 23, 34)})
    table.add_row({"amount": 15, "time": datetime.time(23, 59, 59)})
    assert (
        str(table)
        == """Table: test
+--------------+---------------+--------------+
|   index: int |   amount: int | time: time   |
+==============+===============+==============+
|            0 |            10 | 12:23:34     |
+--------------+---------------+--------------+
|            1 |            15 | 23:59:59     |
+--------------+---------------+--------------+"""
    )


def test_delete_row():
    table = Table("test")
    table.add_column(IntCol("amount"))

    table.add_row({"amount": 10})
    table.add_row({"amount": 20})
    table.add_row({"amount": 30})

    assert table.rows_count == 3

    table.delete_row(1)

    assert table.rows_count == 2
    assert table.get_row(0).values[0] == 10
    assert table.get_row(1).values[0] == 30

    with pytest.raises(IndexError):
        table.delete_row(10)
