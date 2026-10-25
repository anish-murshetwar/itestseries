
from django.contrib import admin

from .models import Chapter, StudyMaterial, Subject


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "is_active", "updated_at")
    list_filter = ("is_active",)
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ("name", "subject", "order", "is_active")
    list_filter = ("subject", "is_active")
    search_fields = ("name", "subject__name")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("subject", "order")


@admin.register(StudyMaterial)
class StudyMaterialAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "chapter",
        "material_type",
        "is_free",
        "is_published",
    )
    list_filter = ("material_type", "is_free", "is_published")
    search_fields = ("title", "chapter__name", "chapter__subject__name")
    prepopulated_fields = {"slug": ("title",)}
