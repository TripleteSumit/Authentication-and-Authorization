from rest_framework.permissions import BasePermission


class HasRole(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        required_roles = getattr(view, "required_role", {})
        role = required_roles.get(request.method, [])
        user_role = request.user.role
        if "__all__" in role or user_role in role:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_superuser:
            return True
        elif user.role == "admin":
            return obj.user == user or obj.user.role in ["moderator", "user"]
        elif user.role == "moderator":
            return obj.user == user or obj.user.role in ["user"]
        elif user.role == "user":
            return obj.user == user
        return False
