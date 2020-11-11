import io
import re
import pikepdf
import requests
from bs4 import BeautifulSoup
from PyPDF2 import PdfFileReader

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    Custom Command for scraping PDFs from Devoirat.net website
    
    You can run it by typing the following command on the terminal
    > py manage.py scrapedevoiratdata

    """

    def handle(self, *args, **kwargs):
        pass