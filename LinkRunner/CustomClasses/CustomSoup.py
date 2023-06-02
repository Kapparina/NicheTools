from bs4 import BeautifulSoup


class Soup(BeautifulSoup):
    def get_links(self) -> dict:
        """Returns all hyperlinks from a Soup object as a dictionary."""
        hyperlinks: dict = {}
        for link in self.find_all("a"):
            hyperlinks[link.text] = link.get("href")
        return hyperlinks
