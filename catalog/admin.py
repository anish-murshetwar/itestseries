from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError

from .models import Board, Chapter, SchoolClass, StudyMaterial, Subject

MAX_PDF_SIZE = 10 * 1024 * 1024  # 10 MB


class StudyMaterialAdminForm(forms.ModelForm):
    pdf_upload = forms.FileField(
        required=False,
        label="PDF file",
        help_text="Upload a PDF (maximum 10 MB). A new upload replaces the stored PDF.",
    )

    class Meta:
        model = StudyMaterial
        exclude = ("file",)

    def clean_pdf_upload(self):
        uploaded = self.cleaned_data.get("pdf_upload")
        if not uploaded:
            return uploaded

        if uploaded.size > MAX_PDF_SIZE:
            raise ValidationError("PDF must be 10 MB or smaller.")

        if not uploaded.name.lower().endswith(".pdf"):
            raise ValidationError("Only PDF files are allowed.")

        header = uploaded.read(5)
        uploaded.seek(0)
        if header != b"%PDF-":
            raise ValidationError("The uploaded file does not appear to be a valid PDF.")

        return uploaded


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(SchoolClass)
class SchoolClassAdmin(admin.ModelAdmin):
    list_display = ("name", "board", "order", "is_active")
    list_filter = ("board", "is_active")
    search_fields = ("name", "board__name")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("board", "order")


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name", "school_class", "is_active", "updated_at")
    list_filter = ("school_class__board", "school_class", "is_active")
    search_fields = ("name", "school_class__name", "school_class__board__name")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ("name", "subject", "order", "is_active")
    list_filter = ("subject__school_class__board", "subject__school_class", "subject", "is_active")
    search_fields = ("name", "subject__name")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("subject", "order")


@admin.register(StudyMaterial)
class StudyMaterialAdmin(admin.ModelAdmin):
    form = StudyMaterialAdminForm
    list_display = (
        "title",
        "chapter",
        "material_type",
        "is_free",
        "is_published",
        "file_size",
    )
    list_filter = (
        "material_type",
        "is_free",
        "is_published",
        "chapter__subject__school_class__board",
        "chapter__subject__school_class",
    )
    search_fields = (
        "title",
        "chapter__name",
        "chapter__subject__name",
        "chapter__subject__school_class__board__name",
    )
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("file_size",)

    def save_model(self, request, obj, form, change):
        uploaded = form.cleaned_data.get("pdf_upload")
        if uploaded:
            obj.file_data = uploaded.read()
            obj.file_name = uploaded.name
            obj.file_size = uploaded.size
            obj.file = ""
        super().save_model(request, obj, form, change)

# iTestSeries Django Admin branding
admin.site.site_header = "iTestSeries Administration"
admin.site.site_title = "iTestSeries Admin"
admin.site.index_title = "Manage iTestSeries"
