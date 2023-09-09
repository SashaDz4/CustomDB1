from Pyro5.api import expose
from typing import Any


@expose
class Row:
    def __init__(self, values: list[Any]) -> None:
        self._values = values

    def __getitem__(self, index: int) -> Any:
        return self._values[index]

    def __setitem__(self, key: int, value: Any) -> None:
        self._values[key] = value

    def __repr__(self) -> str:
        return f'[{", ".join(map(str, self.values))}]'

    @property
    def values(self):
        return self._values
