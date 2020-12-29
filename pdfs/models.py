from django.contrib.postgres.search import (
    TrigramSimilarity,
    SearchVector,
    SearchQuery,
    SearchRank,
)
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone as tz
from bs4 import BeautifulSoup


class LevelManager(models.Manager):

    def get_high_school_stage_levels(self):
        return self.filter(stage=Level.HIGH_SCHOOL_STAGE).order_by('name')

    def get_middle_school_stage_levels(self):
        return self.filter(stage=Level.MIDDLE_SCHOOL_STAGE).order_by('name')

    def get_elementary_school_stage_levels(self):
        return self.filter(stage=Level.ELEMENTARY_SCHOOL_STAGE).order_by('name')


class Subject(models.Model):
    slug = models.SlugField(
        unique=True,
        blank=True,
        null=True
    )
    name = models.CharField(
        'Subject name',
        max_length=100
    )

    def save(self, *args, **kwargs):
        """
        Save Slug before inserting the row into the DB
        """
        if not self.id:
            self.slug = slugify(self.name)
        super(Subject, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('pdfs:subject-detail', kwargs={'subject_slug': self.slug})

    def get_pdfs_count(self):
        return PDF.objects.filter(subject=self).count()

    def get_all_exluding_self(self):
        return Subject.objects.exclude(name=self.name)


class Section(models.Model):
    """
    Section must have an instance with 'tout' as name and slug so that urlpatterns
    works as expected
    It will be created automatically when calling PDF.get_section()
    """
    slug = models.SlugField(
        unique=True,
        blank=True,
        null=True
    )
    name = models.CharField(
        'Section name',
        max_length=100
    )

    def save(self, *args, **kwargs):
        """
        Save Slug before inserting the row into the DB
        """
        if not self.id:
            self.slug = slugify(self.name)
        super(Section, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('pdfs:section-detail', kwargs={'section_slug': self.slug})

    def get_pdfs_count(self):
        return PDF.objects.filter(section=self).count()

    def is_default(self):
        return self.name == 'tout'

    def get_all_exluding_self(self):
        return Section.objects.exclude(name=self.name)


class Level(models.Model):
    ELEMENTARY_SCHOOL_STAGE = 'elementary'
    MIDDLE_SCHOOL_STAGE = 'middle'
    HIGH_SCHOOL_STAGE = 'high'
    PDF_SCHOOL_STAGES = [
        (ELEMENTARY_SCHOOL_STAGE, 'elementary'),
        (MIDDLE_SCHOOL_STAGE, 'middle'),
        (HIGH_SCHOOL_STAGE, 'high'),
    ]

    slug = models.SlugField(
        unique=True,
        blank=True,
        null=True
    )
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

    def save(self, *args, **kwargs):
        """
        Save Slug before inserting the row into the DB
        """
        if not self.id:
            self.slug = slugify(self.name)
        super(Level, self).save(*args, **kwargs)

    objects = LevelManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('pdfs:level-detail', kwargs={'level_slug': self.slug})

    def get_pdfs_count(self):
        return PDF.objects.filter(level=self).count()

    def get_all_exluding_self(self):
        return Level.objects.exclude(name=self.name)


class Category(models.Model):
    slug = models.SlugField(
        unique=True,
        blank=True,
        null=True
    )
    name = models.CharField(
        'Category name',
        max_length=100
    )

    def save(self, *args, **kwargs):
        """
        Save Slug before inserting the row into the DB
        """
        if not self.id:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('pdfs:category-detail', kwargs={'category_slug': self.slug})

    def __str__(self):
        return self.name

    def get_pdfs_count(self):
        return PDF.objects.filter(category=self).count()

    def get_all_exluding_self(self):
        return Category.objects.exclude(name=self.name)


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


class PDFManager(models.Manager):
    """Manager for PDF Model"""
    def search(self, query):
        """
        Search for PDFs with ranking and Trigram similarity
        """
        search_vector = SearchVector('title')
        search_query = SearchQuery(query)
        pdfs = PDF.objects.annotate(
            similarity=TrigramSimilarity('title', query),
            rank=SearchRank(search_vector, search_query)
        ).filter(
            similarity__gt=0.1,
        ).order_by('-rank')

        return pdfs


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

    objects = PDFManager()
    _cached_soup = None
    
    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse('pdfs:devoir-detail', kwargs={'pdf_slug': self.slug})

    def get_level(self):
        return self.level

    def get_section(self):
        if self.section:
            return self.section
        else:
            return Section.objects.get_or_create(name='tout')[0]

    def get_subject(self):
        return self.subject

    def get_category(self):
        return self.category

    def get_html_content_body(self):
        if self.html_file:
            soup = None
            if self._cached_soup:
                soup = self._cached_soup
            else:
                html_file = self.html_file.open('r')
                soup = BeautifulSoup(html_file, 'lxml')
                self._cached_soup = soup

            devoir_content = soup.find("div", {"id":"page-container"})

            return devoir_content
        return None

    def get_html_content_head(self):
        if self.html_file:
            soup = None
            if self._cached_soup:
                soup = self._cached_soup
            else:
                html_file = self.html_file.open('r')
                soup = BeautifulSoup(html_file, 'lxml')
                self._cached_soup = soup
                
            devoir_content = str(soup.head).replace('<head>', '').replace('</head>', '')

            return devoir_content
        return None


class PDFError(models.Model):
    data = models.TextField(
        'PDF data'
    )
    traceback = models.TextField()
