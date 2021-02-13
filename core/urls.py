"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps import GenericSitemap
from core.sitemaps import StaticViewSitemap
from pdfs.models import (
    PDF,
    Level,
    Section,
    Subject,
    Category,
)


sitemaps = {
    'static': StaticViewSitemap,
    
    'level': GenericSitemap({
        'queryset': Level.objects.all(),
    }, priority=0.5),
    
    'sections': GenericSitemap({
        'queryset': Section.objects.all(),
    }, priority=0.5),
    
    'subject': GenericSitemap({
        'queryset': Subject.objects.all(),
    }, priority=0.5),
    
    'category': GenericSitemap({
        'queryset': Category.objects.all(),
    }, priority=0.5),

    'pdfs': GenericSitemap({
        'queryset': PDF.objects.all(),
    }, priority=1),
}


urlpatterns = [
    path('', include('home.urls')),
    path('admin/', admin.site.urls),
    path('', include('pdfs.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'
    ),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)