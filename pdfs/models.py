from django.db import models
from django.utils import timezone as tz


class LevelManager(models.Manager):

    def get_high_school_stage_levels(self):
        return self.filter(stage=Level.HIGH_SCHOOL_STAGE).order_by('-name')

    def get_middle_school_stage_levels(self):
        return self.filter(stage=Level.MIDDLE_SCHOOL_STAGE).order_by('-name')

    def get_elementary_school_stage_levels(self):
        return self.filter(stage=Level.ELEMENTARY_SCHOOL_STAGE).order_by('-name')


class Subject(models.Model):
    name = models.CharField(
        'Subject name',
        max_length=100
    )

    def __str__(self):
        return self.name

    def get_pdfs_count(self):
        return PDF.objects.filter(subject=self).count()


class Section(models.Model):
    name = models.CharField(
        'Section name',
        max_length=100
    )

    def __str__(self):
        return self.name

    def get_pdfs_count(self):
        return PDF.objects.filter(section=self).count()


class Level(models.Model):
    ELEMENTARY_SCHOOL_STAGE = 'elementary'
    MIDDLE_SCHOOL_STAGE = 'middle'
    HIGH_SCHOOL_STAGE = 'high'
    PDF_SCHOOL_STAGES = [
        (ELEMENTARY_SCHOOL_STAGE, 'elementary'),
        (MIDDLE_SCHOOL_STAGE, 'middle'),
        (HIGH_SCHOOL_STAGE, 'high'),
    ]

    name = models.CharField(
        'Level name',
        max_length=100
    )

    stage = models.CharField(
        'Schooling stage',
        max_length=20,
        choices=PDF_SCHOOL_STAGES,
        default=HIGH_SCHOOL_STAGE,
    )

    objects = LevelManager()

    def __str__(self):
        return self.name

    def get_pdfs_count(self):
        return PDF.objects.filter(level=self).count()


class Category(models.Model):
    name = models.CharField(
        'Category name',
        max_length=100
    )

    def __str__(self):
        return self.name

    def get_pdfs_count(self):
        return PDF.objects.filter(category=self).count()


def pdf_upload_path(instance, filename):
    try:
        return 'docs/{}.pdf'.format(instance.id)
    except:
        return 'docs/{}.pdf'.format(filename)


def html_upload_path(instance, filename):
    try:
        return 'docs/{}.html'.format(instance.id)
    except:
        return 'docs/{}.html'.format(filename)


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
        max_length=250
    )
    slug = models.SlugField(
        'SlugField',
        max_length=250
    )
    title = models.CharField(
        "Title",
        max_length=250,
        null=True,
        blank=True
    )
    description = models.CharField(
        "Description",
        max_length=300,
        null=True,
        blank=True
    )
    size = models.CharField(
        "Pdf size",
        max_length=10,
        null=True,
        blank=True
    )
    pdf_file = models.FileField(
        "PDF file",
        null=True,
        blank=True,
        upload_to=pdf_upload_path
    )
    html_file = models.FileField(
        "The HTML version of the PDF file",
        null=True,
        blank=True,
        upload_to=html_upload_path,
    )
    origin = models.URLField(
        'The origin link that this PDF comes from',
        max_length=512,
    )
    parent_origin = models.URLField(
        'The link\'s page that contains this PDF link',
        max_length=256,
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


class PDFError(models.Model):
    data = models.TextField(
        'PDF data'
    )
    traceback = models.TextField()
