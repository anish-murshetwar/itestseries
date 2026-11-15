from io import BytesIO

from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404, render

from .models import Board, Chapter, StudyMaterial, Subject


def home(request):
    boards = Board.objects.filter(is_active=True).prefetch_related("classes__subjects")
    featured_materials = StudyMaterial.objects.filter(
        is_published=True,
        chapter__is_active=True,
        chapter__subject__is_active=True,
        chapter__subject__school_class__is_active=True,
        chapter__subject__school_class__board__is_active=True,
    ).select_related(
        "chapter", "chapter__subject",
        "chapter__subject__school_class",
        "chapter__subject__school_class__board",
    )[:6]
    return render(request, "catalog/home.html", {
        "boards": boards,
        "featured_materials": featured_materials,
    })


def subject_detail(request, board_slug, class_slug, subject_slug):
    subject = get_object_or_404(
        Subject.objects.select_related("school_class__board"),
        slug=subject_slug,
        school_class__slug=class_slug,
        school_class__board__slug=board_slug,
        is_active=True,
        school_class__is_active=True,
        school_class__board__is_active=True,
    )
    chapters = subject.chapters.filter(is_active=True).annotate(
        material_count=Count("materials", filter=Q(materials__is_published=True))
    )
    return render(request, "catalog/subject_detail.html", {
        "subject": subject,
        "chapters": chapters,
    })


def chapter_detail(request, board_slug, class_slug, subject_slug, chapter_slug):
    chapter = get_object_or_404(
        Chapter.objects.select_related(
            "subject", "subject__school_class", "subject__school_class__board"
        ),
        slug=chapter_slug,
        subject__slug=subject_slug,
        subject__school_class__slug=class_slug,
        subject__school_class__board__slug=board_slug,
        subject__is_active=True,
        subject__school_class__is_active=True,
        subject__school_class__board__is_active=True,
        is_active=True,
    )
    materials = chapter.materials.filter(is_published=True)
    return render(request, "catalog/chapter_detail.html", {
        "chapter": chapter,
        "materials": materials,
    })


def material_pdf(request, material_id):
    material = get_object_or_404(
        StudyMaterial,
        pk=material_id,
        is_published=True,
        chapter__is_active=True,
        chapter__subject__is_active=True,
        chapter__subject__school_class__is_active=True,
        chapter__subject__school_class__board__is_active=True,
    )
    if not material.file_data:
        raise Http404("PDF is not available.")
    filename = material.file_name or f"study-material-{material.pk}.pdf"
    response = FileResponse(
        BytesIO(bytes(material.file_data)),
        content_type="application/pdf",
        filename=filename,
    )
    response["X-Content-Type-Options"] = "nosniff"
    return response


def search(request):
    query = request.GET.get("q", "").strip()
    material_type = request.GET.get("type", "")
    materials = StudyMaterial.objects.filter(
        is_published=True,
        chapter__is_active=True,
        chapter__subject__is_active=True,
        chapter__subject__school_class__is_active=True,
        chapter__subject__school_class__board__is_active=True,
    ).select_related(
        "chapter", "chapter__subject", "chapter__subject__school_class",
        "chapter__subject__school_class__board",
    )
    if query:
        materials = materials.filter(
            Q(title__icontains=query)
            | Q(description__icontains=query)
            | Q(chapter__name__icontains=query)
            | Q(chapter__subject__name__icontains=query)
        )
    if material_type in StudyMaterial.MaterialType.values:
        materials = materials.filter(material_type=material_type)
    page_obj = Paginator(materials, 12).get_page(request.GET.get("page"))
    return render(request, "catalog/search.html", {
        "page_obj": page_obj,
        "query": query,
        "selected_type": material_type,
        "material_types": StudyMaterial.MaterialType.choices,
    })
