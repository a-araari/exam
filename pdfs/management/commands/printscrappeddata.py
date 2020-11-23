from django.core.management.base import BaseCommand
from pdfs.models import(
    PDF,
    Level,
    Section,
    Subject,
    Category,
    PDFError,
)


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        print('Printing Scrapped PDFs data..')

        pdfs_count = PDF.objects.all().count()
        levels_count = Level.objects.all().count()
        sections_count = Section.objects.all().count()
        subjects_count = Subject.objects.all().count()
        categories_count = Category.objects.all().count()
        pdf_errors_count = PDFError.objects.all().count()

        print("%-50s%-10s" % ('Scrapped pdfs count:', f'{pdfs_count} pdfs'))
        print("%-50s%-10s" % ('registred levels count:', f'{levels_count} levels'))
        print("%-50s%-10s" % ('registred sections count:', f'{sections_count} sections'))
        print("%-50s%-10s" % ('registred subjects count:', f'{subjects_count} subjects'))
        print("%-50s%-10s" % ('registred categories count:', f'{categories_count} categories'))
        print("%-50s%-10s" % ('Raised errors count:', f'{pdf_errors_count} errors'))
        
        print()

        print("%-50s%-10s" % ('Count of scrapped PDFs without a level:', f'{PDF.objects.filter(level__isnull=True).count()} pdfs'))
        print("%-50s%-10s" % ('Count of scrapped PDFs without a section:', f'{PDF.objects.filter(section__isnull=True).count()} pdfs'))
        print("%-50s%-10s" % ('Count of scrapped PDFs without a subject:', f'{PDF.objects.filter(subject__isnull=True).count()} pdfs'))
        print("%-50s%-10s" % ('Count of scrapped PDFs without a category:', f'{PDF.objects.filter(category__isnull=True).count()} pdfs'))
        print("%-50s%-10s" % ('Unsaved PDFs rate (for total pdfs count):', f'{(pdfs_count * pdf_errors_count) / 50}%'))

