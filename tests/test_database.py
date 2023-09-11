import pytest

from models.database import Database
from models.table import Table


def test_add_table():
    db = Database("test_db")
    db.add_table("test_table")
    assert db.tables_count == 1

    with pytest.raises(ValueError) as exception_info:
        db.add_table("test_table")
    assert (
        exception_info.value.args[0]
        == "Table with name 'test_table' already exists in DB!"
    )
    assert db.tables_count == 1

    db.add_table("another_table")
    assert db.tables_count == 2


def test_get_table():
    db = Database("test_db")
    table_name = "test_table"

    with pytest.raises(KeyError) as exception_info:
        db.get_table(table_name)

    assert (
        exception_info.value.args[0] == "No table with name 'test_table' found in DB!"
    )

    db.add_table(table_name)
    assert db.get_table(table_name).name == table_name


def test_delete_table():
    db = Database("test_db")
    table_name = "test_table"
    db.add_table(table_name)
    assert db.tables_count == 1

    db.delete_table(table_name)
    assert db.tables_count == 0
    with pytest.raises(KeyError):
        db.get_table(table_name)
