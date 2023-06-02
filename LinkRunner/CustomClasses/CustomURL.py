from pathlib import Path
from urllib import request


class URL(str):
    def convert_to_filepath(self) -> Path:
        """Converts a URL to an OS-readable filepath, namely to be used by Windows."""
        return Path(request.url2pathname(self.removeprefix("file:")))
