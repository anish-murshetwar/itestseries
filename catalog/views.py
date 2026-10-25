
from django.db.models import Q,Count
from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator

from .models import Chapter, StudyMaterial, Subject


def home(request):
    subjects = Subject.objects.filter(is_active=True)
    featured_materials = StudyMaterial.objects.filter(
        is_published=True,
        chapter__is_active=True,
        chapter__subject__is_active=True,
    ).select_related("chapter", "chapter__subject")[:6]

    return render(
        request,
        "catalog/home.html",
        {
            "subjects": subjects,
            "featured_materials": featured_materials,
        },
    )


def subject_detail(request, subject_slug):
    subject = get_object_or_404(
        Subject,
        slug=subject_slug,
        is_active=True,
    )
    chapters = (
        subject.chapters.filter(is_active=True)
        .annotate(
            material_count=Count(
                "materials",
                filter=Q(materials__is_published=True),
            )
        )
    )

    return render(
        request,
        "catalog/subject_detail.html",
        {"subject": subject, "chapters": chapters},
    )


def chapter_detail(request, subject_slug, chapter_slug):
    chapter = get_object_or_404(
        Chapter.objects.select_related("subject"),
        slug=chapter_slug,
        subject__slug=subject_slug,
        subject__is_active=True,
        is_active=True,
    )

    materials = chapter.materials.filter(is_published=True)

    return render(
        request,
        "catalog/chapter_detail.html",
        {"chapter": chapter, "materials": materials},
    )



def search(request):
    query = request.GET.get("q", "").strip()
    material_type = request.GET.get("type", "")

    materials = StudyMaterial.objects.filter(
        is_published=True,
        chapter__is_active=True,
        chapter__subject__is_active=True,
    ).select_related("chapter", "chapter__subject")

    if query:
        materials = materials.filter(
            Q(title__icontains=query)
            | Q(description__icontains=query)
            | Q(chapter__name__icontains=query)
            | Q(chapter__subject__name__icontains=query)
        )

    valid_types = StudyMaterial.MaterialType.values
    if material_type in valid_types:
        materials = materials.filter(material_type=material_type)

    paginator = Paginator(materials, 12)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(
        request,
        "catalog/search.html",
        {
            "page_obj": page_obj,
            "query": query,
            "selected_type": material_type,
            "material_types": StudyMaterial.MaterialType.choices,
        },
    )

