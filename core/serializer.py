from django.contrib.auth import password_validation, authenticate
from rest_framework import serializers
from authenticationbackend.utils import validate_incoming_data
from rest_framework_simplejwt.serializers import (
    TokenRefreshSerializer as RefreshSerializer,
    TokenBlacklistSerializer,
)
from rest_framework_simplejwt.exceptions import InvalidToken
from .models import User


class SignUpSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField()

    class Meta:
        model = User
        fields = ("email", "password", "confirm_password", "phone")

    def validate(self, data):
        errors = validate_incoming_data(self.initial_data, list(self.fields.keys()))

        if errors:
            raise serializers.ValidationError({"fields": errors})

        password = data.get("password")
        confirm_password = data.get("confirm_password")

        if password != confirm_password:
            raise serializers.ValidationError(
                {"password": "password and confirm_password doesn't match."}
            )

        password_validation.validate_password(password)
        return data

    def create(self, validated_data):
        validated_data.pop("confirm_password", None)
        user = User.objects.create_user(**validated_data)
        return user


class SignInSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=128, style={"input_type": "password"})

    def validate(self, data):
        request = self.context.get("request")

        user = authenticate(request, **data)

        if not user:
            raise serializers.ValidationError(
                {"credential": "Invalid email or password."}
            )

        if not user.is_active:
            raise serializers.ValidationError({"account": "This account is inactive."})

        data["user"] = user
        return data


class TokenRefreshSerializer(RefreshSerializer):
    refresh = None

    def validate(self, data):
        refresh_token = self.context.get("request").COOKIES.get("refresh", None)

        if not refresh_token:
            raise InvalidToken()

        data["refresh"] = refresh_token
        return super().validate(data)


class LogoutSerializer(TokenBlacklistSerializer):
    refresh = None

    def validate(self, data):
        refresh = self.context.get("request").COOKIES.get("refresh")
        if not refresh:
            raise serializers.ValidationError({"error": "Invalid request."})

        data["refresh"] = refresh
        return super().validate(data)
