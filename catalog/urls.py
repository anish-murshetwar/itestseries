from django.urls import path

from . import views

app_name = "catalog"

urlpatterns = [
    path("", views.home, name="home"),
    path("search/", views.search, name="search"),
    path("materials/<int:material_id>/pdf/", views.material_pdf, name="material_pdf"),
    path(
        "boards/<slug:board_slug>/classes/<slug:class_slug>/subjects/<slug:subject_slug>/",
        views.subject_detail,
        name="subject_detail",
    ),
    path(
        "boards/<slug:board_slug>/classes/<slug:class_slug>/subjects/<slug:subject_slug>/chapters/<slug:chapter_slug>/",
        views.chapter_detail,
        name="chapter_detail",
    ),
]
