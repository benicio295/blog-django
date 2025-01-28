import io
from unittest.mock import MagicMock, patch

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from PIL import Image

from blog.models import Category, Page, Post, Tag


class TestModels(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(name="category mocked")
        cls.tag = Tag.objects.create(name="tag mocked")
        cls.page = Page.objects.create(
            title="page mocked",
            is_published=True,
            content="content mocked",
        )
        cls.post = Post.objects.create(
            title="post mocked",
            excerpt="excerpt mocked",
            is_published=False,
            content="content mocked",
            category=cls.category,
        )
        cls.post.tags.add(cls.tag)  # type: ignore

    def test_tag(self):
        self.assertEqual(self.tag.name, "tag mocked")
        self.assertEqual(len(self.tag.slug), 16)  # type: ignore
        self.assertEqual(self.tag.__str__(), self.tag.name)

    def test_category(self):
        self.assertEqual(self.category.name, "category mocked")
        self.assertEqual(len(self.category.slug), 21)  # type: ignore
        self.assertEqual(self.category.__str__(), self.category.name)

    def test_page(self):
        self.assertEqual(self.page.title, "page mocked")
        self.assertEqual(len(self.page.slug), 17)  # type: ignore
        self.assertEqual(self.page.__str__(), self.page.title)

    def test_post_manager_get_published(self):
        self.assertNotIn(
            self.post,
            Post.objects.get_published(),  # type: ignore
        )
        self.assertEqual(self.post.get_absolute_url(), "/")

    @patch("blog.models.resize_image")
    def test_post(self, mocked_resize_image: MagicMock):
        image = io.BytesIO()
        img = Image.new("RGB", (100, 100), color="red")
        img.save(image, format="PNG")

        self.post.cover = SimpleUploadedFile(  # type: ignore
            name="new-image.png",
            content=image.read(),
            content_type="image/png",
        )
        self.post.is_published = True
        self.post.save()  # type: ignore
        self.assertEqual(self.post.title, "post mocked")
        self.assertEqual(len(self.post.slug), 17)  # type: ignore
        self.assertEqual(
            self.post.get_absolute_url(), f"/post/{self.post.slug}/"
        )
        self.assertEqual(self.post.__str__(), self.post.title)
        mocked_resize_image.assert_called_once()
