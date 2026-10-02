from rest_framework import generics
from rest_framework.permissions import SAFE_METHODS

from .models import Article
from .permissions import IsStaffOrReadOnly
from .serializers import (
    ArticleDetailSerializer,
    ArticleListSerializer,
    ArticleWriteSerializer,
)


class ArticleQuerysetMixin:
    def get_queryset(self):
        articles = Article.objects.prefetch_related("tags")
        if self.request.user.is_staff:
            return articles
        return articles.filter(is_visible=True)


class ArticleListView(ArticleQuerysetMixin, generics.ListAPIView):
    serializer_class = ArticleListSerializer


class ArticleDetailView(ArticleQuerysetMixin, generics.RetrieveUpdateAPIView):
    permission_classes = [IsStaffOrReadOnly]
    lookup_field = "uuid"

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return ArticleDetailSerializer
        return ArticleWriteSerializer
