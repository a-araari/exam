from django.contrib import admin

from pdfs.models import PDF


@admin.register(PDF)
class PDFAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'size', 'pages')
