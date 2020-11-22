from random import randint
from django.core.management.base import BaseCommand

from pdfs.models import (
    PDF,
    Subject,
    Section,
    Level,
    Category,
    PDFError
)


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        yes = input('Are you sure you want to delete the current Database? (Yes/no): ')

        if yes != 'Yes':
            print('Operation canceled!')
            exit(0)

        words = ["Algorithm", "Argument", "Arrays", "Arithmetic operators", "Assignment operators", "Augmented reality", "Autonomous", "Binary numbers"]
        for i in range(3):
            print(f'Rewrite the following numbers to continue please ({i+1}/3):')
            sentence = f'``{words[randint(0, len(words)-1)]} {words[randint(0, len(words)-1)]}``'
            user_input = None
            print()
            print(sentence)
            print()

            while sentence[2:-2] != user_input:
                user_input = input('Type: ')

        print('Deleting PDFs:', PDF.objects.all().delete())
        print('Deleting Subjects:', Subject.objects.all().delete())
        print('Deleting Sections:', Section.objects.all().delete())
        print('Deleting Levels:', Level.objects.all().delete())
        print('Deleting Categorys:', Category.objects.all().delete())
        print('Deleting PDFError:', PDFError.objects.all().delete())

