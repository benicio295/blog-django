from typing import Any

from django.contrib import admin
from django.http import HttpRequest

from site_setup.models import MenuLink, SiteSetup


# Register your models here.
class MenuLinkInline(admin.TabularInline):  # type: ignore
    model = MenuLink
    extra = 0

    def has_module_permission(self, request: HttpRequest) -> bool:
        return not request.user.is_superuser  # type: ignore

    def has_add_permission(
        self, request: HttpRequest, obj: Any | None = None
    ) -> bool:
        return True

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


@admin.register(SiteSetup)
class SiteSetupAdmin(admin.ModelAdmin):  # type: ignore
    list_display = (
        "title",
        "description",
    )
    inlines = (MenuLinkInline,)

    def has_add_permission(self, request: HttpRequest) -> bool:
        return not SiteSetup.objects.exists()

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
