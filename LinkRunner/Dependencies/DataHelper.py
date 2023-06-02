import pandas as pd
from pathlib import Path
from LinkRunner.CustomClasses import URL, Soup, Dict


def create_dataframe(_cols: dict[str, list] | Dict[str, list]) -> pd.DataFrame:
    """Takes a dictionary (or dict-like) parameter and uses it to return a pandas DataFrame."""
    return pd.DataFrame.from_dict(_cols)


def get_data(_url: str) -> Dict:
    """Converts a URL to a filepath before fetching and returning hyperlinks."""
    converted_url: Path = URL(_url).convert_to_filepath()
    soup: Soup = make_soup(converted_url)
    return Dict(soup.get_links())


def make_soup(_url: str | Path) -> Soup:
    """Helper function - Returns a Soup (ala BeautifulSoup) object using an open handle."""
    with open(_url) as fp:
        return Soup(fp, "html5lib")