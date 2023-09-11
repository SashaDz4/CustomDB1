from __future__ import annotations
from Pyro5.api import expose
from interval import Interval

from typing import Any

from tabulate import tabulate

from .column import Column
from .row import Row


@expose
class Table:
    def __init__(self, name: str) -> None:
        self._name = name
        self._columns: list[Column] = []
        self._rows: list[Row] = []

    @property
    def name(self):
        return self._name

    @property
    def rows(self):
        return [[index] + row.values for index, row in enumerate(self._rows)]

    @property
    def columns(self):
        return ["index: int",] + list(
            f"{column.name}: {column.type}" for column in self._columns
        )

    @property
    def rows_count(self):
        return len(self._rows)

    @property
    def columns_count(self):
        return len(self._columns)

    def __str__(self):
        return f"Table: {self.name}\n" + self._str_columns_and_rows()

    def to_str(self):
        return str(self)

    def _str_columns_and_rows(self) -> str:
        if len(self._columns) == 0:
            return ""
        rows = [
            [
                f"{value.lower_bound} - {value.upper_bound}" if isinstance(value, Interval) else value for value in row
            ]
            for row in self.rows
        ]
        return tabulate(
            rows,
            headers=self.columns,
            tablefmt="grid",
        )

    def _get_column_names(self) -> tuple[Any, ...]:
        return tuple(column.name for column in self._columns)

    def _check_column_name_already_exists(self, new_column_name: str) -> bool:
        return new_column_name in self._get_column_names()

    def add_column(self, column: Column) -> Column:
        if self._check_column_name_already_exists(column.name):
            raise ValueError(
                f"Column with name '{column.name}' already exists in the table!"
            )

        self._columns.append(column)
        self._add_default_values_to_all_existing_rows(column)
        return column

    def _add_default_values_to_all_existing_rows(self, column: Column) -> None:
        for row in self._rows:
            row.values.append(column.default)

    def _validate_row_data(self, data: dict[str, Any]) -> None:
        if len(data) == 0:
            raise ValueError("Row data cannot be empty!")

        columns_names = self._get_column_names()
        if not set(data.keys()).issubset(set(columns_names)):
            raise ValueError(
                f"Invalid column names: {tuple(data.keys())} is not subset of {columns_names}!"
            )

    def add_row(self, data: dict[str, Any]) -> Row:
        self._validate_row_data(data)

        row = []

        for column in self._columns:
            value_to_add = data.get(column.name, None)

            if not value_to_add:  # handle default case
                row.append(column.default)
                continue

            column.validate_or_error(value_to_add)

            row.append(value_to_add)

        created_row = Row(row)
        self._rows.append(created_row)
        return created_row

    def get_row(self, index: int) -> Row:
        if not (0 <= index < len(self._rows)):
            raise IndexError(f"Row with index '{index}' does not exist!")

        return self._rows[index]

    def get_column_by_name(self, name: str) -> Column:
        return next(column for column in self._columns if column.name == name)

    def change_row(self, index: int, data: dict) -> None:
        row = self.get_row(index)
        self._validate_row_data(data)

        # validate all values pass validation
        for column_name, new_column_value in data.items():
            column = self.get_column_by_name(column_name)
            column.validate_or_error(new_column_value)

        for column_name, new_column_value in data.items():
            column_index = self._get_column_names().index(column_name)
            row[column_index] = new_column_value

    def remap_items(self, items, new_order: list[int]) -> list:
        pairs = sorted([(items[i], idx) for i, idx in enumerate(new_order)], key=lambda x: x[1])
        return [pair[0] for pair in pairs]

    def change_columns(self, new_order: list[int]) -> Table:
        if len(set(new_order)) != len(self._columns):
            raise ValueError(
                f"New order should contain {len(self._columns)} different elements!"
            )
        if max(new_order) >= len(self._columns) or min(new_order) < 0:
            raise ValueError(
                f"New order should contain values from 1 to {len(self._columns)}!"
            )
        for row in self._rows:
            row._values = self.remap_items(row, new_order)
        self._columns = self.remap_items(self._columns, new_order)
        return self

    def rename_column(self, old_name: str, new_name: str) -> Table:
        if self._check_column_name_already_exists(new_name):
            raise ValueError(
                f"Column with name '{new_name}' already exists in the table!"
            )

        column = self.get_column_by_name(old_name)
        column._name = new_name
        return self

    def delete_row(self, index: int) -> Row:
        """Delete row by index, and return it"""
        row = self.get_row(index)
        del self._rows[index]
        return row
