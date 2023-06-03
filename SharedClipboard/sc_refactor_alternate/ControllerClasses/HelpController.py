class Help:
    def __init__(self, blurb_text: str, help_text: str):
        self.blurb_text = blurb_text
        self.help_text = help_text

    def read_blurb(self) -> str:
        return self.blurb_text

    def read_help(self) -> str:
        return self.help_text
