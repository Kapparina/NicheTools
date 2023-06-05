import regex


def remove_chars(user_string: str, value: str) -> str:
    """Removes selected characters from a given string."""
    return str(regex.sub(
        pattern=rf"({value})",
        repl=rf"",
        string=rf"{user_string}",
        flags=regex.VERBOSE)
    )


def part_filter(user_string: str, keep_parts: int = 2) -> list:
    if len(user_string.split()) > 1:
        return user_string.split()[0:0 + keep_parts]
    else:
        return [user_string, None]
