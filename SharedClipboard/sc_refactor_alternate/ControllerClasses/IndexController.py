class Index:
    """Used to index dictionaries, allowing index-based queries."""
    def __init__(self, data: dict):
        self._data = data
        self._index = [i for i in enumerate(self.data, 1)]

# ------------ Properties: ------------

    @property
    def data(self) -> dict:
        """The data property."""
        return self._data

    @data.setter
    def data(self, value: dict) -> None:
        self._data = value

    @data.deleter
    def data(self) -> None:
        del self._data

    @property
    def index(self) -> list:
        return [i for i in enumerate(self.data, 1)]

# ------------ Methods: ------------

    def check_index(self, key: str) -> str | bool:
        """Checks if the key is in the enumerated index of the passed dictionary."""
        if key.isdigit():
            try:
                k = key
                key = next(key for i, key in self.index if i == int(k))
            except StopIteration:
                pass
        if key in self.data.keys():
            return key
        else:
            return False
