import os
from django.core.management.base import BaseCommand

from pdfs.models import PDF
from ._pdf_to_html_converter import convert_pdf_to_html


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        print('Loading PDFs..')
        
        pdfs = PDF.objects.filter(html_file='')
        print(f'start converting ({pdfs.count()} pdfs)...')

        for pdf in pdfs:
            print(f'Processing PDF with ID={pdf.id}')
            try:
                html_temp_file_path = convert_pdf_to_html(pdf.pdf_file.file.name)
                if html_temp_file_path:
                    with open(html_temp_file_path, 'rb') as file:
                        pdf.html_file.save(pdf.title, file)
                        print(f'Successfully converting PDF with ID={pdf.id}')

                os.remove(html_temp_file_path) # Delete file when done

            except Exception as e:
                print(f'Exception raised while converting PDF with ID={pdf.id}:', repr(e))