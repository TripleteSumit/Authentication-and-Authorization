from django.db import models
from core.models import User


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment")
    updated_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comment_updated_by", null=True
    )
    message = models.CharField(
        max_length=255,
        blank=True,
    )
    attachment = models.FileField(upload_to="comment_attachment", null=True, blank=True)
    archived = models.BooleanField(default=False)  # use for soft delete
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
