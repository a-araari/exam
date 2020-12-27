from django.urls import path

from pdfs.views import (
    devoir_detail,
    devoir_pdf_detail,
    devoir_html_detail,

    level_detail,
    section_detail,
    subject_detail,
    category_detail,

    level_section_detail,
    level_section_subject_detail,
    level_section_subject_category_detail,
)


app_name = 'pdfs'

"""
Understand by examples:
    (1) https://exercice.net/devoir-controle-premiere-annee-1992-1993/
    (2) https://exercice.net/devoir-controle-premiere-annee-1992-1993/pdf/
    (3) https://exercice.net/devoir-controle-premiere-annee-1992-1993/html/

    # ---------------------------------------------------------------------

    (1) https://exercice.net/1-ere/
    (2) https://exercice.net/informatique/
    (3) https://exercice.net/Algorithme/
    (4) https://exercice.net/devoirs/

    # ---------------------------------------------------------------------

    (1) https://exercice.net/1-ere/informatique/
    (2) https://exercice.net/1-ere/informatique/Algorithme/
    (3) https://exercice.net/1-ere/informatique/Algorithme/devoirs/

"""

urlpatterns = [
    path('devoir/<str:pdf_slug>/', devoir_detail, name='devoir-detail'),
    path('devoir/<str:pdf_slug>/pdf/', devoir_pdf_detail, name='devoir-pdf-detail'),
    path('devoir/<str:pdf_slug>/html/', devoir_html_detail, name='devoir-html-detail'),

    # ---------------------------------------------------------------------

    path('level/<str:level_slug>/', level_detail, name='level-detail'),
    path('section/<str:section_slug>/', section_detail, name='section-detail'),
    path('subject/<str:subject_slug>/', subject_detail, name='subject-detail'),
    path('category/<str:category_slug>/', category_detail, name='category-detail'),

    # ---------------------------------------------------------------------

    path(
        '<str:level_slug>/<str:section_slug>/',
        level_section_detail,
        name='level-section-detail'
    ),
    path(
        '<str:level_slug>/<str:section_slug>/<str:subject_slug>/',
        level_section_subject_detail,
        name='level-section-subject-detail'
    ),
    path(
        '<str:level_slug>/<str:section_slug>/<str:subject_slug>/<str:category_slug>/',
        level_section_subject_category_detail,
        name='level-section-subject-category-detail'
    ),
]