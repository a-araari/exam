import io
import os
import re
import pikepdf
import requests
from bs4 import BeautifulSoup

from django.core.management.base import BaseCommand

from pdfs.models import (
    PDF,
    Subject,
    Level,
    Category,
    Section
)


class AbstractScraper(BaseCommand):
    """
    Custom Command for scraping PDFs from Devoirat.net website
    
    You can run it by typing the following command on the terminal
    > py manage.py scrape{Your script sub-name}data

    """
    urls_list = None
    main_url = ''
    stage = PDF.HIGH_SCHOOL_STAGE # default stage
    pdf_link_re = r'^.+\.([pP][dD][fF])(.*)$'
    total = 0

    def handle(self, *args, **kwargs):
        counter = 0
        for url in self.urls_list:
            try:
                counter += 1
                print('-'*3 + str(counter) + '-'*3, f'crawling {url}:')

                response = requests.get(url)
                soup = BeautifulSoup(response.content, 'html.parser')

                # getting section name
                section_name = self.get_section_name(soup)

                self.extract_pdfs(soup, url, section_name)
            except Exception as e:
                print(repr(e))

    def extract_pdfs(self, soup, url, section_name):
        """
        Extracting all PDFs from a web page

        @param: soup: BeautifulSoup4 object contains page data
        """
        sub_counter = 0
        for a in soup.find_all('a', {"class": "cc-m-download-link"}, href=True):
            sub_counter += 1
            self.total += 1

            try:
                link_content= a['href']

                if not re.match(self.pdf_link_re, link_content):
                    continue

                pdf_href = f"{self.main_url}{a['href']}"
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

                dc_creator = None
                dc_title = None
                dc_description = None
                dc_subject = None

                with io.BytesIO(response.content) as f:
                    pdfIO = pikepdf.open(f)

                    meta_data = pdfIO.open_metadata()
                    dc_creator = meta_data.get('dc:creator')
                    dc_title = meta_data.get('dc:title')
                    dc_description = meta_data.get('dc:description')
                    dc_subject = meta_data.get('dc:subject')

                self.save_pdf(
                    title,
                    description,
                    file_name,
                    file_type,
                    file_size,
                    dc_creator,
                    dc_title,
                    dc_description,
                    dc_subject,
                    url,
                    response,
                    section_name,
                    pdf_href
                )

            except Exception as e:
                print(repr(e))

    def save_pdf(self,title, description, file_name, file_type, file_size, dc_creator, dc_title, dc_description, dc_subject, url, response, section_name, pdf_href):
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
            parent_origin=url,
            origin=pdf_href,
        )

        temporarylocation="file.pdf"
        with open(temporarylocation,'wb') as out:
            out.write(io.BytesIO(response.content).read())

        with open(temporarylocation, 'rb') as read:
            pdf_instance.file.save(file_name, read)

        os.remove(temporarylocation) # Delete file when done
        
        subject_name = self.get_subject(url)
        if subject_name:
            subject, created = Subject.objects.get_or_create(name=subject_name)
            pdf_instance.subject = subject

        level_name = self.get_level(url)
        if level_name:
            level, created = Level.objects.get_or_create(name=level_name)
            pdf_instance.level = level

        category_name = self.get_category(url)
        if category_name:
            category, created = Category.objects.get_or_create(name=category_name)
            pdf_instance.category = category

        if section_name:
            section, created = Section.objects.get_or_create(name=section_name)
            pdf_instance.section = section

        pdf_instance.stage = self.stage

        pdf_instance.save()
        print()
        print(
            '     %-10s%-50s%-30s%-15s%-10s%-10s%-10s' % (
                f"{'-'*3}{self.total}{'-'*3}",
                file_name,
                description,
                subject_name,
                section_name,
                level_name,
                category_name,
            )
        )

    def get_section_name(self, soup):
        try:
            for h1 in soup.find_all('h1'):
                contents = h1.contents

                if contents:
                    content = contents[0]
                    splitted = content.split(':')

                    if 'section' in splitted[0].strip().lower():
                        section_name = splitted[1].strip().lower()

                        if splitted[1].strip() in ('Sciences expérimentales', 'Sciences Exp', 'Sciences Expérimentales'):
                            return 'sciences expérimentales'

                        return section_name
        except:
            return None

    def get_subject(self, url):
        """
        Must be overridden
        """
        pass

    def get_level(self, url):
        """
        Must be overridden
        """
        pass

    def get_category(self, url):
        """
        Must be overridden
        """
        pass
