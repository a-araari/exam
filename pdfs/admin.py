from django.contrib import admin

from pdfs.models import (
    PDF,
    Subject,
    Section,
    Level,
    Category,
    PDFError,
)


@admin.register(PDF)
class PDFAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'subject', 'section', 'level', 'category')
    list_filter = ('stage', 'category', 'section', 'level', 'subject')
    search_fields = ('title', )


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_pdfs_count')

    def get_pdfs_count(self, instance, *args, **kwargs):
        return instance.get_pdfs_count()

    get_pdfs_count.short_description = 'related pdfs count'


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_pdfs_count')

    def get_pdfs_count(self, instance, *args, **kwargs):
        return instance.get_pdfs_count()

    get_pdfs_count.short_description = 'related pdfs count'
    filter_horizontal = ('subjects', )


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_pdfs_count')

    def get_pdfs_count(self, instance, *args, **kwargs):
        return instance.get_pdfs_count()

    get_pdfs_count.short_description = 'related pdfs count'
    filter_horizontal = ('subjects', )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_pdfs_count')

    def get_pdfs_count(self, instance, *args, **kwargs):
        return instance.get_pdfs_count()
        
    get_pdfs_count.short_description = 'related pdfs count'


@admin.register(PDFError)
class PDFErrorAdmin(admin.ModelAdmin):
    list_display = ('get_error',)

    def get_error(self, instance, *args, **kwargs):
        t = instance.traceback
        return t.strip()[t.strip().rindex('\n'):]
    
    get_error.short_description = 'Error'