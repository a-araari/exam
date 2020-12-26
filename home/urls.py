from django.urls import path

from home.views import (
    search,
    index,
)


app_name = 'home'

urlpatterns = [
    path('', index, name='index'),
    path('search/', search, name='search'),
]