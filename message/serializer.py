import os
from rest_framework import serializers
from .models import Comment
from authenticationbackend.utils import validate_incoming_data


class CommentSerializer(serializers.ModelSerializer):
    message = serializers.CharField(max_length=255)

    def validate(self, data):
        errors = validate_incoming_data(
            self.initial_data, ["message"], ["attachment"], self.partial
        )
        if errors:
            raise serializers.ValidationError({"errors": errors})
        attachment = data.get("attachment")
        if attachment and (
            attachment.size > 5 * 1024 * 1024
            or os.path.splitext(attachment.name)[1].lower()
            not in [".doc", ".docx", ".pdf", ".jpeg", ".jpg", ".png"]
        ):
            raise serializers.ValidationError(
                {
                    "attachment": "Invalid attachment. Make sure attachment comes under these extension (.doc, .docx, .pdf, .jpeg, .jpg, .png) and must not exceed 5MB in size."
                }
            )
        return data

    class Meta:
        model = Comment
        fields = ("id", "message", "attachment")
