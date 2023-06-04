class Help:
    def __init__(self, blurb_text: str = str(), help_text: str = str()):
        self._blurb = blurb_text
        self._help = help_text

# ------------ Properties: ------------

    @property
    def blurb(self) -> str:
        """The blurb property."""
        return self._blurb

    @blurb.setter
    def blurb(self, text: str) -> None:
        self._blurb = text

    @blurb.deleter
    def blurb(self) -> None:
        del self._blurb

    @property
    def help(self) -> str:
        """The help property."""
        return self._help

    @help.setter
    def help(self, text: str) -> None:
        self._help = text

    @help.deleter
    def help(self) -> None:
        del self._help
