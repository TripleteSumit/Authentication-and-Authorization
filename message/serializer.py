import os
from rest_framework import serializers
from core.models import User
from .models import Comment
from authenticationbackend.utils import validate_incoming_data


class CommentUserSerailizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "role")


class CommentSerializer(serializers.ModelSerializer):
    message = serializers.CharField(max_length=255)
    created_by = CommentUserSerailizer(source="user", read_only=True)
    updated_by = CommentUserSerailizer(read_only=True)

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
        fields = ("id", "message", "attachment", "created_by", "updated_by")
