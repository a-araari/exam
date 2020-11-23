from ._abstract_scraper import AbstractScraper
from ._devoir_main_urls import (
    URLS,
    get_subject as devoir_get_subject,
    get_level as devoir_get_level,
    get_category as devoir_get_category,
)

from pdfs.models import PDF


class Command(AbstractScraper):
    urls_list = URLS
    main_url = 'https://www.devoir.tn/'
    stage = PDF.MIDDLE_SCHOOL_STAGE
    pdf_download_button_class = 'btn-download'

    def get_subject(self, url):
        return devoir_get_subject(url)

    def get_level(self, url):
        return devoir_get_level(url)

    def get_category(self, url):
        return devoir_get_category(url)

    def get_section_name(self, soup):
        try:
            section_name = soup.find_all('p', {"class": 'm-0 fs-14'})[-1].contents[0]
            levels = ['7ème', '8ème', '9ème', '1ère', '2ème', '3ème', '4ème', 'bac']

            section_name = section_name.replace('année', '')
            for level in levels:
                if level in section_name:
                    section_name = section_name.replace(level, '')
                    break

            return section_name.strip()
        except:
            return ''

    def get_extra_pdf_info(self, pdf_anchor_tag):
        parent_div = pdf_anchor_tag.parent

        title = parent_div.find("h5").find("strong").contents[0].strip()
        description = None
        try:
            description = parent_div.find("h5").find("small").contents[2].strip()
            if '•' in description: description = description[:-2].strip()
        except:
            pass

        file_name = title
        file_type = None
        file_size = None

        return title, description, file_name, file_type, file_size

    def get_stage(self, url):
        if 'primaire' in url: return PDF.ELEMENTARY_SCHOOL_STAGE
        if 'base' in url: return PDF.MIDDLE_SCHOOL_STAGE
        
        return PDF.HIGH_SCHOOL_STAGE
