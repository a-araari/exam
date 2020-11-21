from ._abstract_scraper import AbstractScraper
from ._devoirat_main_urls import (
    URLS,
    get_subject as devoirat_get_subject,
    get_level as devoirat_get_level,
    get_category as devoirat_get_category,
)


class Command(AbstractScraper):
    urls_list = URLS
    main_url = 'https://www.devoirat.net/'

    def get_subject(self, url):
        """
        Must be overridden
        """
        return devoirat_get_subject(url)

    def get_level(self, url):
        """
        Must be overridden
        """
        return devoirat_get_level(url)

    def get_category(self, url):
        """
        Must be overridden
        """
        return devoirat_get_category(url)
