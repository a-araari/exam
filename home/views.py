from django.shortcuts import render
from django.utils.translation import gettext as _


def index(request):
    context = {
        'title': _('Home'),
    }

    return render(request, 'home/index.html', context)


def search(request):
    q = None
    title = _('Searching for exams, series and courses')

    if request.method == 'GET':
        q = request.GET.get('q')
        if q:
            print(q)
            title = _('Searching for: ') + q

    context = {
        'title': title,
    }

    return render(request, 'home/search.html', context)