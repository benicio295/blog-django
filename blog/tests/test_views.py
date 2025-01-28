from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from blog.models import Category, Page, Post, Tag


class TestViews(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="MockedUser", password="MockedPassword"
        )
        self.category = Category.objects.create(name="Category Mocked")
        self.tag = Tag.objects.create(name="Tag Mocked")
        self.page = Page.objects.create(
            title="Page Mocked",
            is_published=True,
            content="content mocked page",
        )
        self.post = Post.objects.create(
            title="Title Post Mocked",
            excerpt="Excerpt Post Mocked",
            content="Content Post Mocked",
            is_published=True,
            created_by=self.user,
            category=self.category,
        )
        self.post.tags.add(self.tag)  # type: ignore

    def test_post_list_view(self):
        response = self.client.get(reverse("blog:index"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/pages/index.html")
        self.assertEqual(len(response.context["posts"]), 1)
        self.assertEqual(response.context["page_title"], "Home")

    def test_page_detail_view(self):
        response = self.client.get(
            reverse("blog:page", kwargs={"slug": self.page.slug})
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/pages/page.html")
        self.assertEqual(
            response.context["page_title"], f"{self.page.title} - Página"
        )
        self.assertEqual(response.context["page"], self.page)
        self.assertEqual(response.context["page"].is_published, True)

    def test_post_detail_view(self):
        response = self.client.get(
            reverse("blog:post", kwargs={"slug": self.post.slug})
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/pages/post.html")
        self.assertEqual(
            response.context["page_title"], f"{self.post.title} - Página"
        )
        self.assertEqual(response.context["post"], self.post)
        self.assertEqual(response.context["post"].is_published, True)

    def test_created_by_list_view_when_has_user_and_no_first_name(self):
        response = self.client.get(
            reverse("blog:created_by", kwargs={"author_pk": self.user.pk})
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["page_title"], f"Página de {self.user.username}"
        )
        self.assertIn(self.post, response.context["posts"])

    def test_created_by_list_view_when_has_user_and_first_name(self):
        self.user.first_name = "First Name"
        self.user.save()
        response = self.client.get(
            reverse("blog:created_by", kwargs={"author_pk": self.user.pk})
        )
        self.assertEqual(
            response.context["page_title"],
            f"Página de {self.user.first_name} {self.user.last_name}",
        )

    def test_created_by_list_view_when_has_no_user(self):
        User.objects.all().delete()
        response = self.client.get(
            reverse("blog:created_by", kwargs={"author_pk": self.user.pk})
        )
        self.assertEqual(response.status_code, 404)

    def test_category_list_view(self):
        response = self.client.get(
            reverse("blog:category", kwargs={"slug": self.category.slug})
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.post, response.context["posts"])
        self.assertEqual(
            response.context["page_title"],
            f"{self.tag.name} - categoria",
        )

    def test_category_list_view_when_category_does_not_exist(self):
        response = self.client.get(
            reverse("blog:category", kwargs={"slug": "mocked-slug"})
        )
        self.assertEqual(response.status_code, 404)

    def test_tag_view(self):
        response = self.client.get(
            reverse("blog:tag", kwargs={"slug": self.tag.slug})
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.post, response.context["posts"])
        self.assertEqual(
            response.context["page_title"],
            f"{self.tag.name} - tags",
        )

    def test_tag_view_when_tag_does_not_exist(self):
        response = self.client.get(
            reverse("blog:tag", kwargs={"slug": "mocked-slug"})
        )
        self.assertEqual(response.status_code, 404)

    def test_search_list_view(self):
        search_value = "Post"[:20]
        response = self.client.get(
            reverse("blog:search"), data={"search": search_value}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.post, response.context["posts"])
        self.assertEqual(len(response.context["posts"]), 1)
        self.assertEqual(
            response.context["page_title"], f"Busca por '{search_value}'"
        )
        self.assertEqual(response.context["search_value"], search_value)

    def test_search_list_view_when_no_search_term(self):
        response = self.client.get(reverse("blog:search"))
        self.assertRedirects(response, reverse("blog:index"))
