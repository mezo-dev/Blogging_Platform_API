from django.urls import path

from .views import ArticleDetailView, ArticleListView

urlpatterns = [
    path("articles/", ArticleListView.as_view(), name="article-list"),
    path("articles/<uuid:uuid>/", ArticleDetailView.as_view(), name="article-detail"),
]
