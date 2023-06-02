import regex


def remove_chars(user_string: str, value: str) -> str:
    """Removes selected characters from a given string."""
    return str(regex.sub(
        pattern=rf"({value})",
        repl=rf"",
        string=rf"{user_string}",
        flags=regex.VERBOSE)
    )
