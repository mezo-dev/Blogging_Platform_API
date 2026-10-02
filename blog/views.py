from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Article
from .serializers import ArticleSerializer


@api_view(http_method_names=["GET"])
def list_articles_view(request):
    articles = Article.objects.filter(is_visible=True).prefetch_related("tags")
    serializer = ArticleSerializer(articles, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(http_method_names=["GET"])
def article_detail_view(request, pk):
    try:
        article = Article.objects.get(is_visible=True, uuid__startswith=pk)
        serializer = ArticleSerializer(article)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Article.DoesNotExist:
        return Response(
            {"message": f'Article with this id "{pk}"dose not exsit.'},
            status=status.HTTP_404_NOT_FOUND,
        )
    except Article.MultipleObjectsReturned:
        return Response(
            {"message": "Ambiguous id, provide more characters."},
            status=status.HTTP_400_BAD_REQUEST,
        )
