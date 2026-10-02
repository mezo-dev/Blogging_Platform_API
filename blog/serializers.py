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
            "tags",
            "created_at",
            "updated_at",
        ]


class ArticleDetailSerializer(ArticleListSerializer):
    class Meta(ArticleListSerializer.Meta):
        fields = [*ArticleListSerializer.Meta.fields, "content", "is_visible"]


class ArticleWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = [
            "title",
            "content",
            "tags",
            "is_visible",
        ]

    def to_representation(self, instance):
        return ArticleDetailSerializer(instance, context=self.context).data
