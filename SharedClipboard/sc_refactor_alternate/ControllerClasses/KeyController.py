import pyperclip as pc


class Key:
    def __init__(self, data: dict):
        self._data = data

# ------------ Properties: ------------

    @property
    def data(self) -> dict:
        """The data property."""
        return self._data

    @data.setter
    def data(self, new_data: dict) -> None:
        self._data = new_data

    @data.deleter
    def data(self) -> None:
        del self._data

# ------------ Methods: ------------

    def key_check(self, key: str) -> bool:
        if key in self.data.keys():
            return True
        else:
            return False

    def save_key(self, key: str) -> bool | None:
        if key.isdigit():
            return False
        elif len(key.strip()) < 1:
            return None
        else:
            self.data[key] = pc.paste()
            return True

    def load_key(self, key: str) -> bool:
        """Loads a value from the class' dictionary."""
        if key in self.data:
            pc.copy(self.data[key])
            return True
        else:
            return False

    def delete_key(self, key: str) -> bool:
        """Deletes a given key from the class' dictionary."""
        if key in self.data.keys():
            self.data.pop(key)
            return True
        else:
            return False

    def wipe_data(self):
        self.data.clear()
        return True
