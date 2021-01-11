import base64

from django.views.decorators.http import require_GET
from django.core.paginator import (
    PageNotAnInteger,
    Paginator,
    EmptyPage,
)
from django.shortcuts import (
    render,
    get_object_or_404
)
from django.http import (
    Http404,
    HttpResponse,
    JsonResponse
)
from pdfs.models import (
    Subject,
    Section,
    Level,
    Category,
    PDF,
)


def devoir_detail(request, pdf_slug):
    """
    Display devoir detail
    This function will raise Http404 if no devoir
    found within the given pdf_slug value

    :param pdf_slug: the target PDF's slug
    :return: HTML response
    """
    devoir = get_object_or_404(PDF, slug=pdf_slug)

    context = {
        'title': devoir.title,
        'devoir': devoir,
    }

    return render(request, 'pdfs/devoir-detail.html', context)


def devoir_pdf_detail(request, pdf_slug):
    """
    Display devoir detail as PDF file
    This function will raise Http404 if no devoir
    found within the given pdf_slug value

    :param pdf_slug: the target PDF's slug
    :return: HTML response
    """
    devoir = get_object_or_404(PDF, slug=pdf_slug)

    context = {
        'title': devoir.title,
        'devoir': devoir,
    }

    return render(request, 'pdfs/devoir-pdf-detail.html', context)


def devoir_html_detail(request, pdf_slug):
    """
    Display devoir detail as HTML file
    This function will raise Http404 if no devoir
    found within the given pdf_slug value

    :param pdf_slug: the target PDF's slug
    :return: HTML response
    """
    devoir = get_object_or_404(PDF, slug=pdf_slug)

    context = {
        'title': devoir.title,
        'devoir': devoir,
    }

    return render(request, 'pdfs/devoir-html-detail.html', context)


def devoir_download(request, pdf_slug):
    devoir = get_object_or_404(PDF, slug=pdf_slug)

    if devoir.pdf_file:
        as_base64 = request.GET.get('as_base64', False)

        if as_base64:
            data = devoir.pdf_file.read()
            base64_data = base64.b64encode(data).decode("utf-8")
            
            data = {
                'base64_data': base64_data
            }
            return JsonResponse(data)
            
        else:
            response = HttpResponse(devoir.pdf_file.open('rb').read(), content_type="application/pdf")
            response['Content-Disposition'] = 'inline; filename=' + f'{devoir.title}.pdf'
            return response

    else:
        raise Http404()


def level_detail(request, level_slug):
    """
    Display level detail
    This function will raise Http404 if no level found
    within the given level_slug value

    :param level_slug: Level slug
    :return: HTML response
    """
    level = get_object_or_404(Level, slug=level_slug)

    context = {
        'title': level.name,
        'level': level,
    }

    return render(request, 'pdfs/level-detail.html', context)


def section_detail(request, section_slug):
    """
    Display section detail
    This function will raise Http404 if no section found
    within the given section_slug value

    :param section_slug: Section slug
    :return: HTML response
    """
    section = get_object_or_404(Section, slug=section_slug)
    context = {
        'title': section.name,
        'section': section,
    }

    return render(request, 'pdfs/section-detail.html', context)


def subject_detail(request, subject_slug):
    """
    Display subject detail
    This function will raise Http404 if no subject found
    within the given subject_slug value

    :param subject_slug: Subject slug
    :return: HTML response
    """
    subject = get_object_or_404(Subject, slug=subject_slug)
    context = {
        'title': subject.name,
        'subject': subject,
    }

    return render(request, 'pdfs/subject-detail.html', context)


def category_detail(request, category_slug):
    """
    Display category detail
    This function will raise Http404 if no category found
    within the given category_slug value

    :param category_slug: Category slug
    :return: HTML response
    """
    category = get_object_or_404(Category, slug=category_slug)
    context = {
        'title': category.name,
        'category': category,
    }

    return render(request, 'pdfs/category-detail.html', context)


def level_section_detail(request, level_slug, section_slug):
    """
    Display level_section detail
    This function will raise Http404 if no level, section found
    within the given level_slug, section_slug values

    :param level_slug: Level slug
    :param: section_slug: Section slug
    :return: HTML response
    """
    level = get_object_or_404(Level, slug=level_slug)
    section = get_object_or_404(Section, slug=section_slug)

    context = {
        'title': f'{level.name}-{section.name}',
        'level': level,
        'section': section,
    }

    return render(request, 'pdfs/level-section-detail.html', context)


def level_section_subject_detail(request, level_slug, section_slug, subject_slug):
    """
    Display level_section_subject detail
    This function will raise Http404 if no level, section, subject found
    within the given level_slug, section_slug, subject_slug values

    :param level_slug: Level slug
    :param: section_slug: Section slug
    :param: subject_slug: Subject slug
    :return: HTML response
    """
    level = get_object_or_404(Level, slug=level_slug)
    section = get_object_or_404(Section, slug=section_slug)
    subject = get_object_or_404(Subject, slug=subject_slug)
    categories = Category.objects.all()

    page = request.GET.get('page', 1)
    max_subjects_per_page = request.GET.get('max_subjects_per_page', 9)

    if not section.is_default():
        subjects = section.subjects.all()
    else:
        subjects = level.subjects.all()

    subjects_count = subjects.count()

    paginator = Paginator(subjects, max_subjects_per_page)
    try:
        subjects = paginator.page(page)
    except PageNotAnInteger:
        subjects = paginator.page(1)
    except EmptyPage:
        subjects = paginator.page(paginator.num_pages)

    context = {
        'title': f'{level.name}-{section.name}-{subject.name}',
        'level': level,
        'section': section,
        'subject': subject,
        'subjects': subjects,
        'categories': categories,
        'subjects_count': subjects_count,
    }

    return render(request, 'pdfs/level-section-subject-detail.html', context)


def level_section_subject_category_detail(request, level_slug, section_slug, subject_slug, category_slug):
    """
    Display level_section_subject_category detail
    This function will raise Http404 if no level, section, subject, category found
    within the given level_slug, section_slug, subject_slug, category_slug values

    :param level_slug: Level slug
    :param: section_slug: Section slug
    :param: subject_slug: Subject slug
    :param: category_slug: Category slug
    :return: HTML response
    """
    level = get_object_or_404(Level, slug=level_slug)
    section = get_object_or_404(Section, slug=section_slug)
    subject = get_object_or_404(Subject, slug=subject_slug)
    category = get_object_or_404(Category, slug=category_slug)

    page = request.GET.get('page', 1)
    max_pdfs_per_page = request.GET.get('max_pdfs_per_page', 9)

    pdfs = PDF.objects.filter(
        level=level,
        subject=subject,
        category=category
    )
    if not section.is_default():
        pdfs.filter(section=section)

    pdfs_count = pdfs.count()

    paginator = Paginator(pdfs, max_pdfs_per_page)
    try:
        pdfs = paginator.page(page)
    except PageNotAnInteger:
        pdfs = paginator.page(1)
    except EmptyPage:
        pdfs = paginator.page(paginator.num_pages)

    context = {
        'title': f'{level.name}-{section.name}-{subject.name}-{category.name}',
        'pdfs': pdfs,
        'level': level,
        'section': section,
        'subject': subject,
        'category': category,
        'pdfs_count': pdfs_count,
    }

    return render(request, 'pdfs/level-section-subject-category-detail.html', context)



@require_GET
def get_level_subjects(request):
    level_slug = request.GET.get('level')
    subjects = None
    data = {}

    if level_slug == 'all':
        subjects = Subject.objects.all().values('slug', 'name')

    elif level_slug:
        level = get_object_or_404(Level, slug=level_slug)
        subjects = level.get_subjects().values('slug', 'name')

    if subjects:
        for i in range(subjects.count()):
            data[i] = subjects[i]

    return JsonResponse(data)


@require_GET
def get_level_sections(request):
    level_slug = request.GET.get('level')
    sections = None
    data = {}

    if level_slug == 'all':
        sections = Section.objects.all().values('slug', 'name')

    elif level_slug:
        level = get_object_or_404(Level, slug=level_slug)
        sections = level.get_sections().values('slug', 'name')

    if sections:
        for i in range(sections.count()):
            data[i] = sections[i]

    return JsonResponse(data)


@require_GET
def get_section_subjects(request):
    section_slug = request.GET.get('section')
    subjects = None
    data = {}

    if section_slug == 'all':
        subjects = Subject.objects.all().values('slug', 'name')

    elif section_slug:
        section = get_object_or_404(Section, slug=section_slug)
        subjects = section.get_subjects().values('slug', 'name')

    if subjects:
        for i in range(subjects.count()):
            data[i] = subjects[i]

    return JsonResponse(data)
