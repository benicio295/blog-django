from typing import Any

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django_summernote.models import AbstractAttachment  # type: ignore

from utils.images import resize_image
from utils.rands import slugify_new

# Create your models here.


# Summernote config on image upload
class PostAttachment(AbstractAttachment):
    def save(self, *args: Any, **kwargs: Any):
        if not self.name:
            self.name = self.file.name

        current_file_name = str(self.file.name)
        super().save(*args, **kwargs)  # type: ignore
        file_changed = False

        if self.file:
            file_changed = current_file_name != self.file.name

        if file_changed:
            resize_image(self.file, 900, True, 70)  # type: ignore


class Tag(models.Model):
    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

    name = models.CharField(max_length=255)
    slug = models.SlugField(
        max_length=255, unique=True, null=True, blank=True, default=None
    )

    def save(self, *args, **kwargs):  # type: ignore
        if not self.slug:  # type: ignore
            self.slug = slugify_new(self.name, 5)  # type: ignore
        return super().save(*args, **kwargs)  # type: ignore

    def __str__(self):
        return self.name


class Category(models.Model):
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    name = models.CharField(max_length=255)
    slug = models.SlugField(
        max_length=255, unique=True, null=True, blank=True, default=None
    )

    def save(self, *args, **kwargs):  # type: ignore
        if not self.slug:  # type: ignore
            self.slug = slugify_new(self.name, 5)  # type: ignore
        return super().save(*args, **kwargs)  # type: ignore

    def __str__(self):
        return self.name


class Page(models.Model):
    class Meta:
        verbose_name = "Page"
        verbose_name_plural = "Pages"

    title = models.CharField(max_length=65)
    slug = models.SlugField(
        max_length=255, unique=True, null=False, blank=True, default=""
    )
    is_published = models.BooleanField(
        default=False,
        help_text="Este campo precisará estar marcado para a página ser exibida publicamente.",
    )
    content = models.TextField()

    def save(self, *args, **kwargs):  # type: ignore
        if not self.slug:  # type: ignore
            self.slug = slugify_new(self.title, 5)  # type: ignore
        return super().save(*args, **kwargs)  # type: ignore

    def __str__(self):
        return self.title


class PostManager(models.Manager):  # type: ignore
    def get_published(self):
        return self.filter(is_published=True).order_by("-pk")


class Post(models.Model):
    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    objects = PostManager()

    title = models.CharField(max_length=65)
    slug = models.SlugField(
        max_length=255, unique=True, null=False, blank=True, default=""
    )
    excerpt = models.CharField(max_length=150)
    is_published = models.BooleanField(
        default=False,
        help_text="Este campo precisará estar marcado para o post ser exibido publicamente.",
    )
    content = models.TextField()
    cover = models.ImageField(upload_to="posts/%Y/%m/", blank=True, default="")
    cover_in_post_content = models.BooleanField(
        default=True,
        help_text="Se marcado, exibirá a capa dentro do post.",
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )  # Adiciona a data de criação do registro
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="post_created_by",
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )  # Atualiza a data a cada atualização do registro.
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="post_updated_by",
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, default=None
    )
    tags = models.ManyToManyField(Tag, blank=True, default="")  # type: ignore

    def __str__(self):
        return self.title

    # Retorna a URL absoluta para a página do post (também é o botao "Ver no site" para o post)
    def get_absolute_url(self):
        if not self.is_published:
            return reverse("blog:index")
        return reverse("blog:post", args=(self.slug,))

    def save(self, *args, **kwargs):  # type: ignore
        if not self.slug:
            self.slug = slugify_new(self.title, 5)
        current_cover_name = str(
            self.cover.name
        )  # pegando o cover antes de salvar no DB
        super_save = super().save(*args, **kwargs)  # type: ignore
        cover_changed = False

        if self.cover:
            cover_changed = (
                current_cover_name != self.cover.name
            )  # o cover foi alterado? Compare com o que está salvo no DB

        if cover_changed:
            resize_image(self.cover, 900)

        return super_save
