from LinkRunner.Dependencies import StringHelper
from typing import Any


def dict_cleanup(data: dict, target: str) -> dict:
    """Removes specific characters and returns a dictionary containing amended keys."""
    clean_data: dict = {}
    for key in list(data):
        clean_data[_key := StringHelper.remove_chars(user_string=key,
                                                     value=rf"{target}")] = data[key]
    return clean_data


def filter_values(data: dict, values: iter) -> dict:
    """Takes a dictionary, removes key: value pairs matching a number of values; returns amended dictionary."""
    _data = data
    for _value in values:
        _data.pop(find_key(data=_data, value=_value))
    return _data


def find_key(data: dict, value: str) -> Any | bool:
    """Returns the key/s holding specified value/s."""
    for _key, _value in data.items():
        if _value == value:
            return _key
    else:
        return False
