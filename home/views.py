from django.shortcuts import render
from django.utils.translation import gettext as _
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from pdfs.models import (
    Level,
    PDF,
)


def index(request):
    high_school_stage_levels = Level.objects.get_high_school_stage_levels()
    middle_school_stage_levels = Level.objects.get_middle_school_stage_levels()
    elementary_school_stage_levels = Level.objects.get_elementary_school_stage_levels()
    
    context = {
        'title': _('Home'),
        'high_school_stage_levels': high_school_stage_levels,
        'middle_school_stage_levels': middle_school_stage_levels,
        'elementary_school_stage_levels': elementary_school_stage_levels,
    }

    return render(request, 'home/index.html', context)


def search(request):
    pdfs = None
    q = request.GET.get('q')
    page = request.GET.get('page', 1)
    max_pdfs_per_page = request.GET.get('docs_per_page', 8)

    title = _('Searching for exams, series and courses')
    high_school_stage_levels = Level.objects.get_high_school_stage_levels()
    middle_school_stage_levels = Level.objects.get_middle_school_stage_levels()
    elementary_school_stage_levels = Level.objects.get_elementary_school_stage_levels()

    if q:
        title = _('Searching for: ') + q
        pdfs = PDF.objects.filter(title__contains=q)
    
        paginator = Paginator(pdfs, max_pdfs_per_page)
        try:
            pdfs = paginator.page(page)
        except PageNotAnInteger:
            pdfs = paginator.page(1)
        except EmptyPage:
            pdfs = paginator.page(paginator.num_pages)

    context = {
        'high_school_stage_levels': high_school_stage_levels,
        'middle_school_stage_levels': middle_school_stage_levels,
        'elementary_school_stage_levels': elementary_school_stage_levels,
        'title': title,
        'pdfs': pdfs,
        'query': q,
    }

    return render(request, 'home/search.html', context)