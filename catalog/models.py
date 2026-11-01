from django.db import models


class Subject(models.Model):
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=170, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Chapter(models.Model):
    subject = models.ForeignKey(
        Subject,
        on_delete=models.PROTECT,
        related_name="chapters",
    )
    name = models.CharField(max_length=180)
    slug = models.SlugField(max_length=200)
    order = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "name"]
        constraints = [
            models.UniqueConstraint(
                fields=["subject", "slug"],
                name="uq_chapter_subject_slug",
            ),
            models.UniqueConstraint(
                fields=["subject", "order"],
                name="uq_chapter_subject_order",
            ),
        ]

    def __str__(self):
        return f"{self.subject.name} - {self.name}"


class StudyMaterial(models.Model):
    class MaterialType(models.TextChoices):
        NOTES = "notes", "Notes"
        QUESTION_PAPER = "question_paper", "Question Paper"
        TEST_PAPER = "test_paper", "Test Paper"
        SOLUTION = "solution", "Solution"
        OTHER = "other", "Other"

    chapter = models.ForeignKey(
        Chapter,
        on_delete=models.PROTECT,
        related_name="materials",
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220)
    material_type = models.CharField(
        max_length=30,
        choices=MaterialType.choices,
        default=MaterialType.NOTES,
    )
    description = models.TextField(blank=True)

    # New persistent storage: PDF bytes are stored in PostgreSQL.
    file_data = models.BinaryField(blank=True, null=True, editable=False)
    file_name = models.CharField(max_length=255, blank=True)
    file_size = models.PositiveBigIntegerField(default=0)

    # Retained temporarily so existing database rows migrate safely.
    # New uploads use file_data, not this local-filesystem field.
    file = models.FileField(
        upload_to="study_materials/%Y/%m/",
        blank=True,
    )

    is_free = models.BooleanField(default=True)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["title"]
        constraints = [
            models.UniqueConstraint(
                fields=["chapter", "slug"],
                name="uq_material_chapter_slug",
            ),
        ]
        indexes = [
            models.Index(
                fields=["chapter", "is_published"],
                name="idx_material_chapter_pub",
            ),
            models.Index(
                fields=["material_type", "is_published"],
                name="idx_material_type_pub",
            ),
        ]

    def __str__(self):
        return self.title
