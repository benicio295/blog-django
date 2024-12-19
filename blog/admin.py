from typing import Any

from django.contrib import admin
from django.forms import ModelForm
from django.http import HttpRequest
from django_summernote.admin import SummernoteModelAdmin
from django_summernote.widgets import mark_safe

from blog.models import Category, Page, Post, Tag


# Register your models here.
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):  # type: ignore
    list_display = ["id", "name", "slug"]
    list_display_links = ("name",)
    search_fields = ["name", "slug"]
    list_per_page = 10  # type: ignore
    ordering = ("-id",)
    prepopulated_fields = {"slug": ("name",)}

    def has_module_permission(self, request: HttpRequest) -> bool:
        return not request.user.is_superuser  # type: ignore

    def has_view_permission(
        self, request: HttpRequest, obj: Any | None = ...
    ) -> bool:
        return not request.user.is_superuser  # type: ignore

    def has_change_permission(
        self, request: HttpRequest, obj: Any | None = ...
    ) -> bool:
        return not request.user.is_superuser  # type: ignore

    def has_delete_permission(
        self, request: HttpRequest, obj: Any | None = ...
    ) -> bool:
        return not request.user.is_superuser  # type: ignore

    def has_add_permission(self, request: HttpRequest) -> bool:
        return True


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):  # type: ignore
    list_display = ["id", "name", "slug"]
    list_display_links = ("name",)
    search_fields = ["name", "slug"]
    list_per_page = 10  # type: ignore
    ordering = ("-id",)
    prepopulated_fields = {"slug": ("name",)}

    def has_module_permission(self, request: HttpRequest) -> bool:
        return not request.user.is_superuser  # type: ignore

    def has_view_permission(
        self, request: HttpRequest, obj: Any | None = ...
    ) -> bool:
        return not request.user.is_superuser  # type: ignore

    def has_change_permission(
        self, request: HttpRequest, obj: Any | None = ...
    ) -> bool:
        return not request.user.is_superuser  # type: ignore

    def has_delete_permission(
        self, request: HttpRequest, obj: Any | None = ...
    ) -> bool:
        return not request.user.is_superuser  # type: ignore

    def has_add_permission(self, request: HttpRequest) -> bool:
        return True


@admin.register(Page)
class PageAdmin(SummernoteModelAdmin):  # type: ignore
    summernote_fields = ("content",)
    list_display = ["id", "title", "is_published"]
    list_display_links = ("title",)
    search_fields = ["title", "content", "slug"]
    list_per_page = 50  # type: ignore
    ordering = ("-id",)
    prepopulated_fields = {"slug": ("title",)}
    list_filter = ["is_published"]
    list_editable = ["is_published"]

    def has_module_permission(self, request: HttpRequest) -> bool:
        return not request.user.is_superuser  # type: ignore

    def has_view_permission(
        self, request: HttpRequest, obj: Any | None = ...
    ) -> bool:
        return not request.user.is_superuser  # type: ignore

    def has_change_permission(
        self, request: HttpRequest, obj: Any | None = ...
    ) -> bool:
        return not request.user.is_superuser  # type: ignore

    def has_delete_permission(
        self, request: HttpRequest, obj: Any | None = ...
    ) -> bool:
        return not request.user.is_superuser  # type: ignore

    def has_add_permission(self, request: HttpRequest) -> bool:
        return True


@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):  # type: ignore
    summernote_fields = ("content",)
    list_display = ["id", "title", "is_published", "created_by"]
    list_display_links = ("title",)
    search_fields = ["id", "title", "slug", "excerpt", "content"]
    list_per_page = 50  # type: ignore
    ordering = ("-id",)
    prepopulated_fields = {"slug": ("title",)}
    list_filter = ["category", "is_published"]
    list_editable = ["is_published"]
    autocomplete_fields = ["category", "tags"]
    readonly_fields = [
        "created_at",
        "updated_at",
        "updated_by",
        "created_by",
        "link",
    ]

    # Criando um novo campo no admin
    def link(self, obj: Post) -> str:
        if not obj.pk:
            return "-"

        url_do_post = obj.get_absolute_url()
        safe_link = mark_safe(
            f"<a href='{url_do_post}' target='_blank'>Ver Post</a>"
        )
        return safe_link

    def save_model(
        self, request: HttpRequest, obj: Any, form: ModelForm, change: bool
    ):  # change: está alterando (True) ou está criando (False)?
        if change:
            obj.updated_by = request.user
        else:
            obj.created_by = request.user
        obj.save()

    def has_module_permission(self, request: HttpRequest) -> bool:
        return not request.user.is_superuser  # type: ignore

    def has_view_permission(
        self, request: HttpRequest, obj: Any | None = ...
    ) -> bool:
        return not request.user.is_superuser  # type: ignore

    def has_change_permission(
        self, request: HttpRequest, obj: Any | None = ...
    ) -> bool:
        return not request.user.is_superuser  # type: ignore

    def has_delete_permission(
        self, request: HttpRequest, obj: Any | None = ...
    ) -> bool:
        return not request.user.is_superuser  # type: ignore

    def has_add_permission(self, request: HttpRequest) -> bool:
        return True
