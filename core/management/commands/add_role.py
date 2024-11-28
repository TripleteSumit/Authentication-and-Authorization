from typing import Any
from django.core.management import BaseCommand
from django.db.models import Q
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


class Command(BaseCommand):
    help = "User role creation and assign permission to them."

    def handle(self, *args: Any, **options: Any):
        admin_group, admin_created = Group.objects.get_or_create(name="Admin")
        moderator_group, moderator_created = Group.objects.get_or_create(
            name="Moderator"
        )
        user_group, user_created = Group.objects.get_or_create(name="User")

        permission_qs = Permission.objects.filter(
            content_type__app_label__in=["core", "message"]
        )

        admin_group.permissions.set(permission_qs)
        moderator_permissions = permission_qs.exclude(
            content_type__app_label="core", codename__contains="delete"
        )
        moderator_group.permissions.set(moderator_permissions)
        user_permissions = permission_qs.filter(content_type__app_label="message")
        user_group.permissions.set(user_permissions)

        self.stdout.write(
            self.style.SUCCESS("Roles and permissions have been set up successfully.")
        )
