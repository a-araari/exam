import os
import subprocess
from sys import platform
from pathlib import Path
from os.path import dirname

from django.conf import settings


html2pdfEX_path = None
if platform == 'win32':
    html2pdfEX_path = Path(dirname(settings.BASE_DIR)) / "pdf2htmlEX/pdf2htmlEX.exe"

elif platform in ('linux', 'linux2', 'ubuntu'):
    pass
else:
    print('Unsupported Operating System')
    exit(1)


convert_pdf_to_html = None
if platform == 'win32':
    def convert_pdf_to_html(pdf_location):
        temp_file_name = 'file.html'
        FNULL = open(os.devnull, 'w')
        response = str(
            subprocess.run(
                [html2pdfEX_path, '--zoom', '1.3', '--no-drm', '1', pdf_location, temp_file_name],
                stdout=FNULL,
                stderr=subprocess.STDOUT
            )
        )

        if 'returncode=0' not in response.lower():
            return None

        return temp_file_name

elif platform in ('linux', 'linux2', 'ubuntu'):
    #['docker', 'run', '-ti', '--rm', '-v', '/home/exercice/test/:/pdf', 'bwits/pdf2htmlex', 'pdf2htmlEX', '--zoom', '1.3', 'a.pdf']
    def convert_pdf_to_html(pdf_location):
        temp_file_name = 'file.html'
        FNULL = open(os.devnull, 'w')
        response = str(
            subprocess.run(
                ['docker', 'run', '-ti', '--rm', '-v', str(settings.BASE_DIR) + ':/pdf', 'bwits/pdf2htmlex', 'pdf2htmlEX', '--zoom', '1.3', pdf_location, temp_file_name],
                stdout=FNULL,
                stderr=subprocess.STDOUT
            )
        )

        if 'returncode=0' not in response.lower():
            return None

        return temp_file_name
