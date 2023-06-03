class Index:
    """Used to index dictionaries, allowing index-based queries."""
    def __init__(self, data: dict):
        self.data = data
        self._index = [i for i in enumerate(self.data, 1)]

    def check_index(self, key: str) -> str | bool:
        """Checks if the key is in the enumerated index of the passed dictionary."""
        if key.isdigit():
            try:
                k = key
                key = next(key for i, key in self._index if i == int(k))
            except StopIteration:
                pass
        if key in self.data.keys():
            return key
        else:
            return False
