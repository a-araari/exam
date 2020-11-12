import io
import os
import re
import pikepdf
import requests
from bs4 import BeautifulSoup
from PyPDF2 import PdfFileReader

from django.core.management.base import BaseCommand
from .devoirat_main_urls import (
    URLS,
    get_subject,
    get_level,
    get_category,
)
from pdfs.models import (
    PDF,
    Subject,
    Level,
    Category,
    Section
)

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

            # getting section name
            # document.getElementsByTagName('h1')[1].textContent.split(':')[0].includes('Section')
            section_name = None
            for h1 in soup.find_all('h1'):
                contents = h1.contents
                if contents:
                    content = contents[0]
                    splitted = content.split(':')
                    if 'section' in splitted[0].strip().lower():
                        section_name = splitted[1].strip()

            self.extract_pdfs(soup, url, section_name)

    def extract_pdfs(self, soup, url, section_name):
        """
        Extracting all PDFs from a web page

        @param: soup: BeautifulSoup4 object contains page data
        """
        for a in soup.find_all('a', {"class": "cc-m-download-link"}, href=True):
            link_content= a['href']

            if not re.match(pdf_link_re, link_content):
                continue

            pdf_href = f"{devoirat_url}{a['href']}"
            response = requests.get(pdf_href)

            parent_div = a.parent.parent

            title_div = parent_div.parent.find("div", {"class": "cc-m-download-title"})
            description_div = parent_div.parent.find("div", {"class": "cc-m-download-description"})
            file_name_div = parent_div.find("div", {"class": "cc-m-download-file-name"})
            file_info_div = parent_div.find("div", {"class": "cc-m-download-file-info"})
            file_type_div = file_info_div.find("span", {"class": "cc-m-download-file-type"}) if file_info_div else None
            file_size_div = file_info_div.find("span", {"class": "cc-m-download-file-size"}) if file_info_div else None

            title = title_div.contents[0] if title_div else None
            description = description_div.contents[0] if description_div else None
            file_name = file_name_div.contents[0] if file_name_div else None
            file_type = file_type_div.contents[0] if file_type_div else None
            file_size = file_size_div.contents[0] if file_size_div else None
            
            # print ("File Data:")

            # print("%-15s%-15s%-15s" % ('', 'title:', title))
            # print("%-15s%-15s%-15s" % ('', 'file name:', description))
            # print("%-15s%-15s%-15s" % ('', 'description:', file_name))
            # print("%-15s%-15s%-15s" % ('', 'file type:', file_type))
            # print("%-15s%-15s%-15s" % ('', 'file size:', file_size))

            dc_creator = None
            dc_title = None
            dc_description = None
            dc_subject = None
            with io.BytesIO(response.content) as f:
                # pdf = PdfFileReader(f)

                pdfIO = pikepdf.open(f)
                # print()
                # print("%-15s%-15s%-15s" % ('', 'pages count', len(pdfIO.pages)))

                meta_data = pdfIO.open_metadata()
                dc_creator = meta_data.get('dc:creator')
                dc_title = meta_data.get('dc:title')
                dc_description = meta_data.get('dc:description')
                dc_subject = meta_data.get('dc:subject')

                # print("Meta Data:")
                # print("%-15s%-15s%-15s" % ('', 'dc:creator', dc_creator))
                # print("%-15s%-15s%-15s" % ('', 'dc:title', dc_title))
                # print("%-15s%-15s%-15s" % ('', 'dc:description', dc_description))
                # print("%-15s%-15s%-15s" % ('', 'dc:subject', dc_subject))
                print()

            pdf_instance = PDF(
                title=title,
                description=description,
                name=file_name,
                slug=file_name.replace(' ', '-').replace('--', '-'),
                # type=file_type,
                size=file_size,
                dc_creator=dc_creator,
                dc_title=dc_title,
                dc_description=dc_description,
                dc_subject=dc_subject,
            )

            temporarylocation="file.pdf"
            with open(temporarylocation,'wb') as out:
                out.write(io.BytesIO(response.content).read())

            with open(temporarylocation, 'rb') as read:
                pdf_instance.file.save(file_name, read)

            os.remove(temporarylocation) # Delete file when done
            
            subject_name = get_subject(url)
            if subject_name:
                subject, created = Subject.objects.get_or_create(name=subject_name)
                pdf_instance.subject = subject

            level_name = get_level(url)
            if level_name:
                level, created = Level.objects.get_or_create(name=level_name)
                pdf_instance.level = level

            category_name = get_category(url)
            if category_name:
                category, created = Category.objects.get_or_create(name=category_name)
                pdf_instance.category = category

            if section_name:
                section, created = Section.objects.get_or_create(name=section_name)
                pdf_instance.section = section

            pdf_instance.save()
            print('     %-50s%-30s%-15s%-10s%-10s%-10s' % (file_name, description, subject_name, section_name, level_name, category_name))
