from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse


class StaticViewSitemap(Sitemap):
    changefreq = "never"
    priority = 0.9

    def items(self):
        return ['index', 'search']

    def location(self, item):
        return reverse(f'home:{item}')
