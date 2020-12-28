import urllib
from django.db.models import Q
from django.shortcuts import render
from django.utils.translation import gettext as _
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from pdfs.models import (
    Level,
    PDF,
)


def index(request):
    level_manager = Level.objects
    
    context = {
        'title': _('Home'),
        'level_manager': level_manager,
    }

    return render(request, 'home/index.html', context)


def search(request):
    pdfs = None
    q = request.GET.get('q')
    encoded_query = urllib.parse.urlencode({'q': q})
    page = request.GET.get('page', 1)
    max_pdfs_per_page = request.GET.get('docs_per_page', 9)

    title = _('Searching for exams, series and courses')
    level_manager = Level.objects

    if q:
        title = _('Searching for: ') + q

        pdfs = PDF.objects.search(query=q)

        for pdf in pdfs:
            print(pdf.title)
    
        paginator = Paginator(pdfs, max_pdfs_per_page)
        try:
            pdfs = paginator.page(page)
        except PageNotAnInteger:
            pdfs = paginator.page(1)
        except EmptyPage:
            pdfs = paginator.page(paginator.num_pages)

    context = {
        'level_manager': level_manager,
        'title': title,
        'pdfs': pdfs,
        'query': q,
        'encoded_query': encoded_query,
    }

    return render(request, 'home/search.html', context)