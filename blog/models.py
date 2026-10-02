from uuid import uuid7

from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = "Tag"

    def __str__(self):
        return self.name


class Article(models.Model):
    uuid = models.UUIDField(default=uuid7, primary_key=True, editable=False)
    title = models.CharField(max_length=500, unique=True)
    content = models.TextField(max_length=50000)
    is_visible = models.BooleanField(
        default=False,
        help_text="If checked, the article is publicly visible; otherwise it is hidden.",
    )
    tags = models.ManyToManyField(Tag, related_name="articles")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "Article"
        ordering = ("-created_at",)
        indexes = [
            models.Index(fields=["is_visible", "-created_at"]),
        ]

    def __str__(self):
        return self.title
