from django.contrib import admin
from django.contrib.auth.models import Permission
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from .forms import UserChangeForm, UserCreationForm

admin.site.name = "RBAC Model"


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = [
        "email",
        "role",
        "phone",
        "is_staff",
        "is_superuser",
        "is_active",
        "last_login",
    ]
    list_filter = ["is_staff"]
    fieldsets = [
        (None, {"fields": ["email", "password", "role"]}),
        ("Permissions", {"fields": ["is_staff", "is_superuser"]}),
    ]
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "password1", "password2"],
            },
        ),
    ]
    search_fields = ["email"]
    ordering = ["email"]
    filter_horizontal = []


class PermissionAdmin(admin.ModelAdmin):
    list_display = ("name", "codename")


admin.site.register(User, UserAdmin)
admin.site.register(Permission, PermissionAdmin)
