from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Article
from .serializers import (
    ArticleListSerializer,
)


class ArticleListView(APIView):
    def get(self, request):
        articles = Article.objects.prefetch_related("tags")
        serializer = ArticleListSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ArticleDeleteView(APIView):
    def delete(self, request, pk):
        article = Article.objects.get(pk=pk)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
