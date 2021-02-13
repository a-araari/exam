from wand.image import Image
from wand.color import Color

from django.core.management.base import BaseCommand
from tempfile import NamedTemporaryFile
from django.core.files import File
from django.conf import settings

from pdfs.models import PDF


THUMBNAIL_SIZE = '800'


class Command(BaseCommand):
    """
    Generate thumbnails from PDFs
    """
    def handle(self, *args, **kwargs):
        print('Start generating thumbnails..')
        pdfs = PDF.objects.filter(thumbnail__isnull=True)
        total = pdfs.count()
        count = 0

        for pdf in pdfs:
            count += 1
            thumbnail = self.get_thumbnail_from_pdf(pdf.pdf_file)
            if thumbnail:
                pdf.thumbnail = thumbnail
                pdf.save()
                print(f'{count}/{total}   --->   PDF {pdf.id}: {pdf.thumbnail}')
            else:
                print(f'! {count}/{total}   --->   PDF {pdf.id}: Unable to generate a thumbnail')

    def get_thumbnail_from_pdf(self, file):
        try:
            filename = file.name
            img = None
                
            # Convert PDF files
            imgs_pdf = Image(file=file)
            imgs = imgs_pdf.convert('jpeg')

            if imgs:
                img = Image(image=imgs.sequence[0])
                img.background_color = Color('white')
                img.alpha_channel = 'remove'

                # resized and save the converted file
                img.transform(crop='', resize=THUMBNAIL_SIZE)
                img.thumbnail()

                temp = NamedTemporaryFile(delete=False)
                temp.flush()
                temp0 = File(temp)

                with temp0.open('wb') as f:
                    img.save(file=f)

                return temp0.open('rb')

        except Exception as e:
            print(repr(e))

        return None
