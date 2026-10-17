from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Article
from .serializers import ArticleSerializer, ArticleUpdateSerializer


class ArticleListView(APIView):
    def get(self, request):
        articles = Article.objects.prefetch_related("tags")
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ArticleDetailView(APIView):
    def get(self, request, uuid):
        article = get_object_or_404(Article, uuid=uuid)
        return Response(ArticleSerializer(article).data)


class ArticleUpdateView(APIView):
    def put(self, request, uuid):
        article = get_object_or_404(Article, uuid=uuid)
        serializer = ArticleUpdateSerializer(article, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            ArticleUpdateSerializer(article).data, status=status.HTTP_200_OK
        )


class ArticleDeleteView(APIView):
    def delete(self, request, uuid):
        article = Article.objects.get(uuid=uuid)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
