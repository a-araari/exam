import base64

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
        'title': level.slug,
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
        'title': section.slug,
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
        'title': subject.slug,
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
        'title': category.slug,
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

    context = {
        'title': f'{level.name}-{section.name}-{subject.name}',
        'level': level,
        'section': section,
        'subject': subject,
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

    context = {
        'title': f'{level.name}-{section.name}-{subject.name}-{category.name}',
        'level': level,
        'section': section,
        'subject': subject,
        'category': category,
    }

    return render(request, 'pdfs/level-section-subject-category-detail.html', context)
