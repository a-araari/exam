import io
import os
import re
import traceback
from sys import platform
import pikepdf
import requests
from bs4 import BeautifulSoup

from django.core.management.base import BaseCommand

from ._pdf_to_html_converter import convert_pdf_to_html
from pdfs.models import (
    PDF,
    Subject,
    Level,
    Category,
    Section,
    PDFError
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
    pdf_download_button_class = 'cc-m-download-link' # default class

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
        for a in soup.find_all('a', {"class": self.pdf_download_button_class}, href=True):
            sub_counter += 1
            self.total += 1

            try:
                link_content= a['href']

                if not re.match(self.pdf_link_re, link_content):
                    continue

                pdf_href = f"{self.main_url}{a['href']}"
                response = requests.get(pdf_href)

                # GATHERING PDF INFORMATION

                title, description, file_name, file_type, file_size = self.get_extra_pdf_info(a)

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

                # SAVING PDF INFORMATION

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
                    pdf_href,
                )

            except Exception as e:        
                print(repr(e))
                pdf_error = PDFError(
                    data='Pre save',
                    traceback=str(traceback.format_exc())
                )
                pdf_error.save()


    def save_pdf(self, title, description, file_name, file_type, file_size, dc_creator, dc_title, dc_description, dc_subject, url, response, section_name, pdf_href):
        pdf_instance = PDF(
            title           =   title[:250]         if title else title,
            description     =   description[:300]   if description else description,
            name            =   file_name[:250]     if file_name else file_name,
            slug            =   title[:250].replace(' ', '-').replace('--', '-') if title else title,
            size            =   file_size,
            dc_creator      =   dc_creator[:250]    if dc_creator and type(dc_creator) is str else dc_creator,
            dc_title        =   dc_title[:250]      if dc_title and type(dc_title) is str else dc_title,
            dc_description  =   dc_description[:250]if dc_description and type(dc_description) is str else dc_description,
            dc_subject      =   dc_subject[:250]    if dc_subject and type(dc_subject) is str else dc_subject,
            parent_origin   =   url,
            origin          =   pdf_href,
        )

        temporarylocation="file.pdf"
        with open(temporarylocation,'wb') as out:
            out.write(io.BytesIO(response.content).read())

        with open(temporarylocation, 'rb') as read:
            pdf_instance.pdf_file.save(title, read)

        # This block of code is disabled
        # you can convert the scraped PDFs using "convertpdfstohtml" command

        # CONVERTING PDF TO HTML FILE
        # html_file_path = convert_pdf_to_html(temporarylocation)
        # if html_file_path:
        #     with open(html_file_path, 'rb') as read:
        #         pdf_instance.html_file.save(title, read)

        # os.remove(temporarylocation) # Delete file when done
        # os.remove(html_file_path) # Delete file when done
        
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

        try:
            raise Exception('')
            pdf_instance.save()
            print()
            print(
                '     %-10s%-100s%-40s%-15s%-10s%-10s%-10s' % (
                    f"{'-'*3}{self.total}{'-'*3}",
                    title,
                    description,
                    subject_name,
                    section_name,
                    level_name,
                    category_name,
                )
            )
        except Exception as ex:
            pdf_error = PDFError()
            pdf_error.data = f"""
                title           = {str(title)           if title            else 'None'}
                description     = {str(description)     if description      else 'None'}
                file_name       = {str(file_name)       if file_name        else 'None'}
                file_type       = {str(file_type)       if file_type        else 'None'}
                file_size       = {str(file_size)       if file_size        else 'None'}
                dc_creator      = {str(dc_creator)      if dc_creator       else 'None'}
                dc_title        = {str(dc_title)        if dc_title         else 'None'}
                dc_description  = {str(dc_description)  if dc_description   else 'None'}
                dc_subject      = {str(dc_subject)      if dc_subject       else 'None'}
                url             = {str(url)             if url              else 'None'}
                response        = {str(response)        if response         else 'None'}
                section_name    = {str(section_name)    if section_name     else 'None'}
                pdf_href        = {str(pdf_href)        if pdf_href         else 'None'}
            """
            pdf_error.traceback = traceback.format_exc()
            pdf_error.save()
            raise Exception('Cannot save PDF')

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

    def get_extra_pdf_info(self, pdf_anchor_tag):
        """
        Can be overrided
        """
        parent_div = pdf_anchor_tag.parent.parent
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

        return title, description, file_name, file_type, file_size
