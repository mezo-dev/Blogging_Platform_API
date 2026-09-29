from django.contrib import admin

from .models import Article, Tag

admin.site.register(Tag)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ["title", "created_at", "updated_at", "is_visible"]
