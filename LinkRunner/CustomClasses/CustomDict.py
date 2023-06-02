from rapidfuzz import process


class Dict(dict):
    def find_key(self, value: str):
        """A method used by the variant of the built-in dict type; used to streamline key hunting."""
        for _key, _value in self.items():
            if _value == value:
                return _key
        else:
            return f"No key at {value}!"

    def fuzz_keys(self, value: str, scope: int = 3):
        """Uses RapidFuzz to perform a fuzzy search on keys."""
        extraction: list[tuple] = process.extract(
            query=value,
            choices=self.keys(),
            limit=scope
        )
        return extraction

    def fuzz_values(self, value: str, scope: int = 3):
        """Uses RapidFuzz to perform a fuzzy search on values."""
        extraction: list[tuple] = process.extract(
            query=value,
            choices=self.values(),
            limit=scope
        )
        return extraction
