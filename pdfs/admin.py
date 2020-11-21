from django.contrib import admin

from pdfs.models import (
    PDF,
    Subject,
    Section,
    Level,
    Category
)


@admin.register(PDF)
class PDFAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'subject', 'section', 'level', 'category')
    list_filter = ('stage', 'subject', 'section', 'level', 'category')


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
