from django.urls import path

from .views import list_articles_view

urlpatterns = [path("articles/", list_articles_view, name="list_articles_view")]
