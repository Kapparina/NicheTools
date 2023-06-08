from rapidfuzz import process
from collections import namedtuple


class Dict(dict):
    def find_key(self, value: str) -> str | bool:
        """A method used by the variant of the built-in dict type; used to streamline key hunting."""
        for _key, _value in self.items():
            if _value == value:
                return _key
        else:
            return False

    def fuzz_keys(self, value: str, scope: int = 3) -> list[namedtuple]:
        """Uses RapidFuzz to perform a fuzzy search on keys."""
        Result: namedtuple = namedtuple("Result", ["name", "likeness", "index"])
        return [Result._make(result) for result in process.extract(
            query=value,
            choices=self.keys(),
            limit=scope
        )]

    def fuzz_values(self, value: str, scope: int = 3) -> list[namedtuple]:
        """Uses RapidFuzz to perform a fuzzy search on values."""
        Result: namedtuple = namedtuple("Result", ["name", "likeness", "index"])
        return [Result._make(result) for result in process.extract(
            query=value,
            choices=self.keys(),
            limit=scope
        )]
