from uuid import uuid7

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Article, Tag


class ArticleAPITests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.tag = Tag.objects.create(name="django")
        cls.visible = Article.objects.create(
            title="Visible", content="Public content", is_visible=True
        )
        cls.visible.tags.add(cls.tag)
        cls.hidden = Article.objects.create(
            title="Hidden", content="Draft content", is_visible=False
        )

    def detail_url(self, article_uuid):
        return reverse("article-detail", kwargs={"uuid": article_uuid})

    def test_list_returns_only_visible_articles(self):
        response = self.client.get(reverse("article-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        uuids = [item["uuid"] for item in response.data["results"]]
        self.assertEqual(uuids, [str(self.visible.uuid)])

    def test_list_omits_content(self):
        response = self.client.get(reverse("article-list"))

        self.assertNotIn("content", response.data["results"][0])

    def test_list_is_paginated(self):
        response = self.client.get(reverse("article-list"))

        self.assertEqual(response.data["count"], 1)
        self.assertIn("next", response.data)

    def test_list_query_count_does_not_grow_with_articles(self):
        for i in range(5):
            article = Article.objects.create(
                title=f"Extra {i}", content="x", is_visible=True
            )
            article.tags.add(self.tag)

        # count + articles + prefetched tags
        with self.assertNumQueries(3):
            self.client.get(reverse("article-list"))

    def test_detail_returns_visible_article_with_content(self):
        response = self.client.get(self.detail_url(self.visible.uuid))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["content"], "Public content")
        self.assertEqual(response.data["tags"], [{"id": self.tag.id, "name": "django"}])

    def test_detail_hidden_article_returns_404(self):
        response = self.client.get(self.detail_url(self.hidden.uuid))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_detail_unknown_uuid_returns_404(self):
        response = self.client.get(self.detail_url(uuid7()))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_detail_malformed_id_returns_404(self):
        response = self.client.get("/api/articles/1073cc2c/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
