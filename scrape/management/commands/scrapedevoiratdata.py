import io
import re
import pikepdf
import requests
from bs4 import BeautifulSoup
from PyPDF2 import PdfFileReader

from django.core.management.base import BaseCommand
from .devoirat_main_urls import URLS

devoirat_url = 'https://www.devoirat.net/'
pdf_link_re = r'^.+\.([pP][dD][fF])(.*)$'


class Command(BaseCommand):
    """
    Custom Command for scraping PDFs from Devoirat.net website
    
    You can run it by typing the following command on the terminal
    > py manage.py scrapedevoiratdata

    """

    def handle(self, *args, **kwargs):
        for url in URLS:
            print(f'crawling {url}:')

            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')

            self.extract_pdfs(soup)

    def extract_pdfs(self, soup):
        """
        Extracting all PDFs from a web page

        @param: soup: BeautifulSoup4 object contains page data
        """
        for a in soup.find_all('a', {"class": "cc-m-download-link"}, href=True):
            link_content= a['href']

            if re.match(pdf_link_re, link_content):
                pdf_href = f"{devoirat_url}{a['href']}"
                response = requests.get(pdf_href)

                print ("url match: ", pdf_href)

                parent_div = a.parent.parent

                title = parent_div.parent.find("div", {"class": "cc-m-download-title"})
                description = parent_div.parent.find("div", {"class": "cc-m-download-description"})
                file_name = parent_div.find("div", {"class": "cc-m-download-file-name"})
                file_info = parent_div.find("div", {"class": "cc-m-download-file-info"})
                file_type = file_info.find("span", {"class": "cc-m-download-file-type"}) if file_info else None
                file_size = file_info.find("span", {"class": "cc-m-download-file-size"}) if file_info else None

                print ("File Data:")

                # print("%-15s%-15s%-15s" % ('', 'title:', title.contents[0] if title else None))
                print("%-15s%-15s%-15s" % ('', 'file name:', file_name.contents[0] if file_name else None))
                # print("%-15s%-15s%-15s" % ('', 'description:', description.contents[0] if description else None))
                # print("%-15s%-15s%-15s" % ('', 'file type:', file_type.contents[0] if file_type else None))
                print("%-15s%-15s%-15s" % ('', 'file size:', file_size.contents[0] if file_size else None))

                with io.BytesIO(response.content) as f:
                    # pdf = PdfFileReader(f)

                    pdf = pikepdf.open(f)
                    # print()
                    print("%-15s%-15s%-15s" % ('', 'pages count', len(pdf.pages)))

                    meta_data = pdf.open_metadata()
                    # print("Meta Data:")
                    # print("%-15s%-15s%-15s" % ('', 'dc:creator', meta_data.get('dc:creator')))
                    # print("%-15s%-15s%-15s" % ('', 'dc:title', meta_data.get('dc:title')))
                    # print("%-15s%-15s%-15s" % ('', 'dc:description', meta_data.get('dc:description')))
                    # print("%-15s%-15s%-15s" % ('', 'dc:subject', meta_data.get('dc:subject')))
                    print()
