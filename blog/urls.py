from django.urls import path

from .views import ArticleDeleteView, ArticleListView

urlpatterns = [
    path("articles/", ArticleListView.as_view(), name="article-list"),
    # path("articles/<uuid:uuid>/", ArticleDetailView.as_view(), name="article-detail"),
    path(
        "articles/<uuid:pk>/delete/", ArticleDeleteView.as_view(), name="article-delete"
    ),
]
