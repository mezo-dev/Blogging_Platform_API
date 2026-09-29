from uuid import uuid8

from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = "Tag"

    def __str__(self):
        return self.name


class Article(models.Model):
    uuid = models.UUIDField(
        default=uuid8, primary_key=True, editable=False, db_index=True
    )
    title = models.CharField(max_length=500, unique=True)
    content = models.TextField(max_length=50000)
    is_visible = models.BooleanField(
        default=False,
        help_text="If checked, the article is hidden; otherwise it is visible.",
    )
    tag = models.ManyToManyField(Tag, related_name="tags", db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "Article"
        ordering = ("-created_at",)
        indexes = [
            models.Index(fields=["uuid", "title"]),
        ]

    def __str__(self):
        return self.title
