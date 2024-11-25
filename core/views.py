from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializer import SignUpSerializer, SignInSerializer


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
                "errors": serializer.errors,
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
                "errors": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
