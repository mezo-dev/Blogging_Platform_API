from uuid import uuid7

from django.contrib.auth import get_user_model
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


class ArticleUpdateAPITests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.staff = User.objects.create_user("editor", password="x", is_staff=True)
        cls.user = User.objects.create_user("reader", password="x")
        cls.tag = Tag.objects.create(name="django")
        cls.article = Article.objects.create(
            title="Original", content="Body", is_visible=True
        )
        cls.draft = Article.objects.create(
            title="Draft", content="WIP", is_visible=False
        )

    def url(self, article):
        return reverse("article-detail", kwargs={"uuid": article.uuid})

    def test_anonymous_cannot_update(self):
        response = self.client.patch(self.url(self.article), {"title": "Hacked"})

        self.assertIn(
            response.status_code,
            (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN),
        )
        self.article.refresh_from_db()
        self.assertEqual(self.article.title, "Original")

    def test_non_staff_cannot_update(self):
        self.client.force_authenticate(self.user)

        response = self.client.patch(self.url(self.article), {"title": "Hacked"})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_staff_can_update_and_gets_read_shape(self):
        self.client.force_authenticate(self.staff)

        response = self.client.patch(
            self.url(self.article),
            {"title": "Edited", "tags": [self.tag.id]},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Edited")
        self.assertEqual(response.data["tags"], [{"id": self.tag.id, "name": "django"}])

    def test_staff_can_edit_and_publish_draft(self):
        self.client.force_authenticate(self.staff)

        response = self.client.patch(
            self.url(self.draft), {"is_visible": True}, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.draft.refresh_from_db()
        self.assertTrue(self.draft.is_visible)

    def test_duplicate_title_returns_400(self):
        self.client.force_authenticate(self.staff)

        response = self.client.patch(
            self.url(self.article), {"title": "Draft"}, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("title", response.data)

    def test_unknown_tag_returns_400(self):
        self.client.force_authenticate(self.staff)

        response = self.client.patch(
            self.url(self.article), {"tags": [999]}, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
