from LinkRunner.Dependencies import StringHelper


def dict_cleanup(data: iter, target: str) -> dict:
    """Removes specific characters and returns a dictionary containing amended keys."""
    clean_data: dict = {}
    for k in list(data):
        clean_data[_k := StringHelper.remove_chars(user_string=k,
                                                   value=rf"{target}")] = data[k]
    return clean_data
