from django.shortcuts import render, get_object_or_404

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



def level_detail(request, level_name):
    """
    Display level detail
    This function will raise Http404 if no level found
    within the given level_name value

    :param level_name: Level name
    :return: HTML response
    """
    level = get_object_or_404(Subject, name=level_name)
    context = {
        'title': level.name,
        'level': level,
    }

    return render(request, 'pdfs/level-detail.html', context)


def section_detail(request, section_name):
    """
    Display section detail
    This function will raise Http404 if no section found
    within the given section_name value

    :param section_name: Section name
    :return: HTML response
    """
    section = get_object_or_404(Section, name=section_name)
    context = {
        'title': section.name,
        'section': section,
    }

    return render(request, 'pdfs/section-detail.html', context)


def subject_detail(request, subject_name):
    """
    Display subject detail
    This function will raise Http404 if no subject found
    within the given subject_name value

    :param subject_name: Subject name
    :return: HTML response
    """
    subject = get_object_or_404(Level, name=subject_name)
    context = {
        'title': subject.name,
        'subject': subject,
    }

    return render(request, 'pdfs/subject-detail.html', context)


def category_detail(request, category_name):
    """
    Display category detail
    This function will raise Http404 if no category found
    within the given category_name value

    :param category_name: Category name
    :return: HTML response
    """
    category = get_object_or_404(Category, name=category_name)
    context = {
        'title': category.name,
        'category': category,
    }

    return render(request, 'pdfs/category-detail.html', context)



def level_section_detail(request, level_name, section_name):
    """
    Display level_section detail
    This function will raise Http404 if no level, section found
    within the given level_name, section_name values

    :param level_name: Level name
    :param: section_name: Section name
    :return: HTML response
    """
    level = get_object_or_404(Subject, name=level_name)
    section = get_object_or_404(Section, name=section_name)

    context = {
        'title': f'{level.name}-{section.name}',
        'level': level,
        'section': section,
    }

    return render(request, 'pdfs/level-section-detail.html', context)


def level_section_subject_detail(request, level_name, section_name, subject_name):
    """
    Display level_section_subject detail
    This function will raise Http404 if no level, section, subject found
    within the given level_name, section_name, subject_name values

    :param level_name: Level name
    :param: section_name: Section name
    :param: subject_name: Subject name
    :return: HTML response
    """
    level = get_object_or_404(Subject, name=level_name)
    section = get_object_or_404(Section, name=section_name)
    subject = get_object_or_404(Level, name=subject_name)

    context = {
        'title': f'{level.name}-{section.name}-{subject.name}',
        'level': level,
        'section': section,
        'subject': subject,
    }

    return render(request, 'pdfs/level-section-subject-detail.html', context)



def level_section_subject_category_detail(request, level_name, section_name, subject_name, category_name):
    """
    Display level_section_subject_category detail
    This function will raise Http404 if no level, section, subject, category found
    within the given level_name, section_name, subject_name, category_name values

    :param level_name: Level name
    :param: section_name: Section name
    :param: subject_name: Subject name
    :param: category_name: Category name
    :return: HTML response
    """
    level = get_object_or_404(Subject, name=level_name)
    section = get_object_or_404(Section, name=section_name)
    subject = get_object_or_404(Level, name=subject_name)
    category = get_object_or_404(Category, name=category_name)

    context = {
        'title': f'{level.name}-{section.name}-{subject.name}-{category.name}',
        'level': level,
        'section': section,
        'subject': subject,
        'category': category,
    }

    return render(request, 'pdfs/level-section-subject-category-detail.html', context)


