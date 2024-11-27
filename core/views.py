from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import (
    TokenRefreshView as RefreshView,
)
from .serializer import (
    SignUpSerializer,
    SignInSerializer,
    TokenRefreshSerializer,
    LogoutSerializer,
)


class SignUpView(APIView):
    serializer_class = SignUpSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"status": "success", "message": "Successfully signed up."},
                status=status.HTTP_201_CREATED,
            )

        return Response(
            {
                "status": "failed",
                "message": "Invalid data",
                "details": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


class SignInView(APIView):
    serializer_class = SignInSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data.get("user")
            refresh = RefreshToken.for_user(user)

            response_data = {
                "access": str(refresh.access_token),
                "email": user.email,
                "role": user.role,
            }

            response = Response(
                {
                    "status": "success",
                    "message": "Signin Successful.",
                    "data": response_data,
                },
                status=status.HTTP_200_OK,
            )

            refresh_token = str(refresh)
            max_age = 3600 * 24 * 15
            response.set_cookie(
                "refresh", refresh_token, max_age=max_age, httponly=True
            )
            return response

        return Response(
            {
                "status": "failed",
                "message": "Something went wrong.",
                "details": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


class TokenRefreshView(RefreshView):
    serializer_class = TokenRefreshSerializer

    def finalize_response(self, request, response, *args, **kwargs):
        if "refresh" in response.data:
            max_age = 3600 * 24 * 15
            response.set_cookie(
                "refresh", response.data["refresh"], max_age=max_age, httponly=True
            )
            del response.data["refresh"]
        return super().finalize_response(request, response, *args, **kwargs)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LogoutSerializer

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            return Response(
                {"status": "success", "message": "sucessfully signout."},
                status=status.HTTP_200_OK,
            )
        return Response(
            {
                "status": "failed",
                "message": "Invalid data",
                "details": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    def finalize_response(self, request, response, *args, **kwargs):
        response.delete_cookie("refresh")
        return super().finalize_response(request, response, *args, **kwargs)
