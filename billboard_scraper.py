from bs4 import BeautifulSoup
import requests


class BillboardScraper:
    """
    This class is used to scrape the Billboard Hot 100 chart.
    """

    def __init__(self, date: str):
        """
        Initialize the BillboardScraper class.

        Args:
            date (str): The date of the chart to scrape.
        """
        self.url = "https://www.billboard.com/charts/hot-100/" + date
        self.soup = BeautifulSoup(requests.get(self.url).text, "html.parser")

    def get_song_list(self) -> list:
        """
        Get a list of song names from the Billboard Hot 100 chart.

        Returns:
            list: A list of song names.
        """
        title_name: list = self.soup.select(selector='ul li h3')
        title_name = [title.text.strip() for title in title_name]
        return title_name[0:100]
