from django.contrib import admin
from .models import Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "message", "attachment", "archived")
    ordering = ("-id",)


admin.site.register(Comment, CommentAdmin)
