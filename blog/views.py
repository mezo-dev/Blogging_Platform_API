from rest_framework import generics

from .models import Article
from .serializers import ArticleDetailSerializer, ArticleListSerializer


class VisibleArticlesMixin:
    def get_queryset(self):
        return Article.objects.filter(is_visible=True).prefetch_related("tags")


class ArticleListView(VisibleArticlesMixin, generics.ListAPIView):
    serializer_class = ArticleListSerializer


class ArticleDetailView(VisibleArticlesMixin, generics.RetrieveAPIView):
    serializer_class = ArticleDetailSerializer
    lookup_field = "uuid"
