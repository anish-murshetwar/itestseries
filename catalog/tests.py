
from django.test import TestCase
from django.urls import reverse

from .models import Board, Chapter, SchoolClass, StudyMaterial, Subject


class CatalogTestDataMixin:
    def setUp(self):
        self.board = Board.objects.create(
            name="ICSE",
            slug="icse",
            is_active=True,
        )

        self.school_class = SchoolClass.objects.create(
            board=self.board,
            name="Class 10",
            slug="class-10",
            order=10,
            is_active=True,
        )

        self.subject = Subject.objects.create(
            school_class=self.school_class,
            name="Mathematics",
            slug="mathematics",
            description="Mathematics study resources",
            is_active=True,
        )

        self.chapter = Chapter.objects.create(
            subject=self.subject,
            name="Algebra",
            slug="algebra",
            order=1,
            is_active=True,
        )

        self.material = StudyMaterial.objects.create(
            chapter=self.chapter,
            title="Algebra Practice Questions",
            slug="algebra-practice-questions",
            material_type=StudyMaterial.MaterialType.TEST_PAPER,
            description="Practice questions for Algebra",
            is_free=True,
            is_published=True,
        )

        self.chapter_url_kwargs = {
            "board_slug": self.board.slug,
            "class_slug": self.school_class.slug,
            "subject_slug": self.subject.slug,
            "chapter_slug": self.chapter.slug,
        }


class HomepageTests(CatalogTestDataMixin, TestCase):

    def test_homepage_returns_success(self):
        response = self.client.get(reverse("catalog:home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Mathematics")

    def test_inactive_subject_is_hidden(self):
        self.subject.is_active = False
        self.subject.save()

        response = self.client.get(reverse("catalog:home"))

        self.assertNotContains(response, "Mathematics")


class ChapterPageTests(CatalogTestDataMixin, TestCase):

    def test_chapter_page_shows_published_material(self):
        response = self.client.get(
            reverse(
                "catalog:chapter_detail",
                kwargs=self.chapter_url_kwargs,
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Algebra Practice Questions")

    def test_unpublished_material_is_hidden(self):
        self.material.is_published = False
        self.material.save()

        response = self.client.get(
            reverse(
                "catalog:chapter_detail",
                kwargs=self.chapter_url_kwargs,
            )
        )

        self.assertNotContains(response, "Algebra Practice Questions")

    def test_inactive_chapter_returns_404(self):
        self.chapter.is_active = False
        self.chapter.save()

        response = self.client.get(
            reverse(
                "catalog:chapter_detail",
                kwargs=self.chapter_url_kwargs,
            )
        )

        self.assertEqual(response.status_code, 404)


class MaterialSearchTests(CatalogTestDataMixin, TestCase):

    def test_search_finds_material_by_title(self):
        response = self.client.get(
            reverse("catalog:search"),
            {"q": "Algebra Practice"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Algebra Practice Questions")

    def test_search_filters_by_material_type(self):
        response = self.client.get(
            reverse("catalog:search"),
            {"type": StudyMaterial.MaterialType.TEST_PAPER},
        )

        self.assertContains(response, "Algebra Practice Questions")

    def test_search_excludes_unpublished_material(self):
        self.material.is_published = False
        self.material.save()

        response = self.client.get(
            reverse("catalog:search"),
            {"q": "Algebra Practice"},
        )

        self.assertNotContains(response, "Algebra Practice Questions")
