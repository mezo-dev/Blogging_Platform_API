from django.urls import path

from .views import ArticleDeleteView, ArticleDetailView, ArticleListView

urlpatterns = [
    path("articles/", ArticleListView.as_view(), name="article-list"),
    path(
        "articles/<uuid:uuid>/detail/",
        ArticleDetailView.as_view(),
        name="article-detail",
    ),
    path(
        "articles/<uuid:uuid>/delete/",
        ArticleDeleteView.as_view(),
        name="article-delete",
    ),
]
