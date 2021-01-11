import urllib
from django.db.models import Q
from django.shortcuts import render
from django.utils.translation import gettext as _
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from pdfs.models import (
    PDF,
    Level,
    Section,
    Subject,
    Category,
)


def index(request):
    level_manager = Level.objects
    
    context = {
        'title': _('Home'),
        'level_manager': level_manager,
    }

    return render(request, 'home/index.html', context)


def search(request):
    levels = Level.objects.all()
    sections = Section.objects.exclude(slug='tout')
    subjects = Subject.objects.all()
    categories = Category.objects.all()

    pdfs = None
    q = request.GET.get('q')
    level_slug = request.GET.get('level', 'all')
    section_slug = request.GET.get('section', 'all')
    subject_slug = request.GET.get('subject', 'all')
    category_slug = request.GET.get('category', 'all')
    encoded_query = urllib.parse.urlencode({'q': q})
    page = request.GET.get('page', 1)
    max_pdfs_per_page = request.GET.get('docs_per_page', 9)

    title = _('Searching for exams, series and courses')
    level_manager = Level.objects

    if q:
        title = _('Searching for: ') + q
        queryset = PDF.objects

        if level_slug != 'all':
            queryset = queryset.filter(level__slug=level_slug)

        if section_slug != 'all':
            queryset = queryset.filter(section__slug=section_slug)

        if subject_slug != 'all':
            queryset = queryset.filter(subject__slug=subject_slug)

        if category_slug != 'all':
            queryset = queryset.filter(category__slug=category_slug)

        pdfs = queryset.search(query=q)

        paginator = Paginator(pdfs, max_pdfs_per_page)
        try:
            pdfs = paginator.page(page)
        except PageNotAnInteger:
            pdfs = paginator.page(1)
        except EmptyPage:
            pdfs = paginator.page(paginator.num_pages)

    context = {
        'level_manager': level_manager,
        'categories': categories,
        'sections': sections,
        'subjects': subjects,
        'levels': levels,
        'title': title,
        'pdfs': pdfs,
        'query': q,
        'encoded_query': encoded_query,
        'default_category': category_slug,
        'default_section': section_slug,
        'default_subject': subject_slug,
        'default_level': level_slug,
    }

    return render(request, 'home/search.html', context)