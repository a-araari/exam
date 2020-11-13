from django.db import models
from django.utils import timezone as tz


class Subject(models.Model):
    name = models.CharField(
        'Subject name',
        max_length=100
    )

    def __str__(self):
        return self.name


class Section(models.Model):
    name = models.CharField(
        'Section name',
        max_length=100
    )

    def __str__(self):
        return self.name


class Level(models.Model):
    name = models.CharField(
        'Level name',
        max_length=100
    )

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(
        'Category name',
        max_length=100
    )

    def __str__(self):
        return self.name


def pdf_upload_path(instance, filename):
    try:
        return 'docs/{}-{}.pdf'.format(filename, instance.date_stored)
    except:
        return 'docs/{}.pdf'.format(filename)


class PDF(models.Model):
    """
    A model which stores data about a PDF.
    """
    ELEMENTARY_SCHOOL_STAGE = 'elementary'
    MIDDLE_SCHOOL_STAGE = 'middle'
    HIGH_SCHOOL_STAGE = 'high'
    PDF_SCHOOL_STAGES = [
        (ELEMENTARY_SCHOOL_STAGE, 'elementary'),
        (MIDDLE_SCHOOL_STAGE, 'middle'),
        (HIGH_SCHOOL_STAGE, 'high'),
    ]

    subject = models.ForeignKey(
        Subject,
        null=True,
        on_delete=models.SET_NULL
    )
    section = models.ForeignKey(
        Section,
        null=True,
        on_delete=models.SET_NULL
    )
    level = models.ForeignKey(
        Level,
        null=True,
        on_delete=models.SET_NULL
    )
    category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.SET_NULL
    )
    stage = models.CharField(
        'Schooling stage',
        max_length=20,
        choices=PDF_SCHOOL_STAGES,
        default=HIGH_SCHOOL_STAGE,
    )

    name = models.CharField(
        "File name",
        max_length=100
    )
    slug = models.SlugField(
        'SlugField'
    )
    title = models.CharField(
        "Title",
        max_length=100,
        null=True,
        blank=True
    )
    description = models.CharField(
        "Description",
        max_length=250,
        null=True,
        blank=True
    )
    size = models.CharField(
        "Pdf size",
        max_length=10,
        null=True,
        blank=True
    )
    file = models.FileField(
        "PDF file",
        null=True,
        blank=True,
        upload_to=pdf_upload_path
    )
    origin = models.URLField(
        'The origin link that this PDF comes from'
    )
    parent_origin = models.URLField(
        'The link\'s page that contains this PDF link'
    )
    pages = models.IntegerField(
        "Number of Pages in Document",
        null=True,
        blank=True
    )
    date_stored = models.DateTimeField(
        "Date Stored Remotely",
        default=tz.now,
        null=True,
        blank=True
    )
    dc_creator = models.CharField(
        'MetaData: dc:creator',
        max_length=250,
        null=True,
        blank=True
    )
    dc_title = models.CharField(
        'MetaData: dc:title',
        max_length=250,
        null=True,
        blank=True
    )
    dc_description = models.CharField(
        'MetaData: dc:description',
        max_length=250,
        null=True,
        blank=True
    )
    dc_subject = models.CharField(
        'MetaData: dc:subject',
        max_length=250,
        null=True,
        blank=True
    )
    
    def __str__(self):
        return f'{self.name}: By {self.description}'

