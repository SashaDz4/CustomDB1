from Pyro5.api import expose
from models.table import Table


@expose
class Database:
    def __init__(self, name: str):
        self._name = name
        self._tables: dict[str, Table] = {}

    @property
    def name(self):
        return self._name

    @property
    def tables(self):
        return self._tables

    @property
    def tables_count(self):
        return len(self._tables)

    def add_table(self, name: str) -> Table:
        table = Table(name)
        if table.name in self._tables:
            raise ValueError(f"Table with name '{table.name}' already exists in DB!")

        self._tables[table.name] = table
        return table

    def _validate_table_existence(self, name: str) -> None:
        if name not in self._tables:
            raise KeyError(f"No table with name '{name}' found in DB!")

    def get_table(self, name: str) -> Table:
        self._validate_table_existence(name)
        return self._tables[name]

    def delete_table(self, name: str) -> Table:
        table = self.get_table(name)
        del self._tables[name]
        return table
