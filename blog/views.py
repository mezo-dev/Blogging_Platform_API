from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Article
from .serializers import ArticleSerializer


@api_view(http_method_names=["GET"])
def list_articles_view(request):
    articles = Article.objects.all().prefetch_related("tags")
    serializer = ArticleSerializer(articles, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)
