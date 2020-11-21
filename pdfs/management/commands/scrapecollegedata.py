from ._abstract_scraper import AbstractScraper
from ._college_main_urls import (
    URLS,
    get_subject as college_get_subject,
    get_level as college_get_level,
    get_category as college_get_category,
)

from pdfs.models import PDF


class Command(AbstractScraper):
    urls_list = URLS
    main_url = 'https://www.tunisiecollege.net/'
    stage = PDF.MIDDLE_SCHOOL_STAGE

    def get_subject(self, url):
        """
        Must be overridden
        """
        return college_get_subject(url)

    def get_level(self, url):
        """
        Must be overridden
        """
        return college_get_level(url)

    def get_category(self, url):
        """
        Must be overridden
        """
        return college_get_category(url)
