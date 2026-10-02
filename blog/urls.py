from django.urls import path

from .views import article_detail_view, list_articles_view

urlpatterns = [
    path("articles/", list_articles_view, name="list_articles_view"),
    path("articles/<uuid:pk>/", article_detail_view, name="article_detail_view"),
]
