from django.urls import path

from django.contrib.auth import views as auth_views
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
    path("accounts/register/", views.register, name="register"),

    path(
        "accounts/login/",
        auth_views.LoginView.as_view(
            template_name="catalog/login.html"
        ),
        name="login",
    ),

    path(
        "accounts/logout/",
        auth_views.LogoutView.as_view(),
        name="logout",
    ),


    path(
        "accounts/password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="catalog/password_reset.html",
            email_template_name="catalog/password_reset_email.txt",
            subject_template_name="catalog/password_reset_subject.txt",
            extra_context={"stage": "request"},
            success_url="/accounts/password-reset/done/",
        ),
        name="password_reset",
    ),
    path(
        "accounts/password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="catalog/password_reset.html",
            extra_context={"stage": "sent"},
        ),
        name="password_reset_done",
    ),
    path(
        "accounts/reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="catalog/password_reset.html",
            extra_context={"stage": "confirm"},
            success_url="/accounts/reset/complete/",
        ),
        name="password_reset_confirm",
    ),
    path(
        "accounts/reset/complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="catalog/password_reset.html",
            extra_context={"stage": "complete"},
        ),
        name="password_reset_complete",
    ),

]
