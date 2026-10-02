from rest_framework import serializers

from .models import Article, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]


class ArticleListSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Article
        fields = [
            "uuid",
            "title",
            "content",
            "tags",
            "created_at",
            "updated_at",
        ]


class ArticleDetailSerializer(ArticleListSerializer):
    class Meta(ArticleListSerializer.Meta):
        fields = [*ArticleListSerializer.Meta.fields]
