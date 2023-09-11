import os.path
from unittest.mock import patch

import pytest

from models.column import IntCol
from models.database import Database
from models.db_manager import DBManager
from models.table import Table


# fmt: off
@pytest.mark.parametrize(
    "db_manager_method, args",
    [
        (
            "add_table",
            ("test_db",),
        ),
        (
            "get_table",
            ("test_table",),
        ),
        (
            "delete_table",
            ("test_table",),
        ),
    ]
)
# fmt: on
def test_corresponding_database_method_was_called(db_manager_method: str, args: tuple):
    db_manager = DBManager()
    db_manager.create_database("test_db")

    with patch.object(Database, db_manager_method) as mock:
        getattr(db_manager, db_manager_method)(*args)

        mock.assert_called_once()


# fmt: off
@pytest.mark.parametrize(
    "db_manager_method, args",
    [
        (
            "add_column",
            ("test_table", IntCol("amount")),
        ),
        (
            "add_row",
            ("test_table", {},),
        ),
        (
            "change_row",
            ("test_table", 0, {}),
        ),
        (
            "change_columns",
            ("test_table", [0]),
        ),
        (
            "delete_row",
            ("test_table", 0),
        ),
    ],
)
# fmt: on
def test_corresponding_column_method_was_called(db_manager_method: str, args: tuple):
    db_manager = DBManager()
    db_manager.create_database("test_db")

    with patch.object(DBManager, "get_table", return_value=Table("test_table")):
        with patch.object(Table, db_manager_method) as mock:
            getattr(db_manager, db_manager_method)(*args)
            mock.assert_called_once()


def test_access_db_without_creating_or_opening():
    db_manager = DBManager()

    with pytest.raises(ValueError) as exception_info:
        db_manager.add_table("test_table")

    assert (
        exception_info.value.args[0]
        == "You should open or create DB before accessing it!"
    )


def test_save_database_file_creating():
    file_name = "test_db.pkl"
    try:
        db_manager = DBManager()
        db_manager.create_database("test_db")
        db_manager.save_database()

        assert os.path.exists(file_name)
    finally:
        os.remove(file_name)


def test_open_database_is_same_as_saved():
    try:
        db_manager = DBManager()
        db_manager.create_database("test_db")
        db_manager.add_table("test_table")
        db_manager.add_column("test_table", IntCol("amount"))
        db_manager.add_row("test_table", {"amount": 20})

        saved_db = db_manager.db
        path = db_manager.save_database()
        db_manager.open_database(path)
        opened_db = db_manager.db

        assert saved_db.tables_count == opened_db.tables_count
        assert (
            saved_db.get_table("test_table").columns_count
            == opened_db.get_table("test_table").columns_count
        )
        assert (
            saved_db.get_table("test_table").rows_count
            == opened_db.get_table("test_table").rows_count
        )
    finally:
        os.remove("test_db.pkl")
