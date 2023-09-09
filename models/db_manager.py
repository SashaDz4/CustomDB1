from __future__ import annotations

import pickle
from typing import Any

from models.column import Column
from models.database import Database
from models.row import Row
from models.table import Table


class DBManager:
    def __init__(self, db: Database = None) -> None:
        self.db = db

    @property
    def db(self) -> Database:
        if self._db is None:
            raise ValueError("You should open or create DB before accessing it!")

        return self._db

    @db.setter
    def db(self, value: Database) -> None:
        self._db = value

    def create_database(self, name: str) -> None:
        self.db = Database(name)

    def add_table(self, name: str) -> None:
        return self.db.add_table(name)

    def get_table(self, name: str) -> Table:
        return self.db.get_table(name)

    def delete_table(self, name: str) -> Table:
        return self.db.delete_table(name)

    def add_column(self, table_name: str, column: Column) -> None:
        table = self.get_table(table_name)
        return table.add_column(column)

    def add_row(self, table_name: str, data: dict[str, Any]) -> None:
        table = self.get_table(table_name)
        return table.add_row(data)

    def change_row(self, table_name: str, index: int, data: dict[str, Any]) -> None:
        table = self.get_table(table_name)
        return table.change_row(index, data)

    def change_columns(self, table_name: str, new_order: list[int]) -> Table:
        table = self.get_table(table_name)
        return table.change_columns(new_order)

    def rename_column(self, table_name: str, old_name: str, new_name: str) -> Table:
        table = self.get_table(table_name)
        return table.rename_column(old_name, new_name)

    def delete_row(self, table_name: str, index: int) -> Row:
        table = self.get_table(table_name)
        return table.delete_row(index)

    def save_database(self, path_to_save: str = None) -> str:
        if path_to_save is None:
            path_to_save = f"{self.db.name}.pickle"

        with open(path_to_save, "wb") as file:
            pickle.dump(self.db, file)

        return path_to_save

    def open_database(self, path_to_load: str = None) -> None:
        with open(path_to_load, "rb") as file:
            db = pickle.load(file)

        self.db = db
