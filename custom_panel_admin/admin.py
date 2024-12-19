from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group, User

# Register your models here.
admin.site.site_header = "Painel Administrativo Blog"
admin.site.site_title = "Blog"
admin.site.index_title = "Painel Administrativo Blog"

admin.site.unregister(User)


@admin.register(User)
class CustomPanelAdminUser(UserAdmin):
    fieldsets = (
        ("Usuário e Senha", {"fields": ("username", "password")}),
        (
            "Informações Pessoais",
            {"fields": ("first_name", "last_name", "email")},
        ),
        (
            "Permissões",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                )
            },
        ),
    )


admin.site.unregister(Group)
