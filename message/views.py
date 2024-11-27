from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from .models import Comment
from .serializer import CommentSerializer


class CommentView(APIView, LimitOffsetPagination):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(
                {
                    "status": "success",
                    "message": "Successfully Commented.",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {
                "status": "failed",
                "message": "Commenting Failed.",
                "details": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    def get(self, request):
        queryset = Comment.objects.filter(user=request.user, archived=False).order_by(
            "-id"
        )
        page = self.paginate_queryset(queryset, request)
        serializer = self.serializer_class(page, many=True)
        return self.get_paginated_response(
            {
                "status": "success",
                "message": "Successfully fetched all comments.",
                "results": serializer.data,
            }
        )

    def _get_comment(self, request):
        comment_id = request.query_params.get("comment_id")
        if not comment_id or not comment_id.isdigit():
            return None, Response(
                {
                    "status": "failed",
                    "message": (
                        "comment_id is required in query parameter."
                        if not comment_id
                        else "Invalid comment_id."
                    ),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            comment_obj = Comment.objects.get(
                pk=comment_id, user=request.user, archived=False
            )
            return comment_obj, None
        except Comment.DoesNotExist:
            return None, Response(
                {"status": "failed", "message": "Comment not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

    def patch(self, request):
        comment_obj, error_response = self._get_comment(request)
        if error_response:
            return error_response

        serializer = self.serializer_class(comment_obj, request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "status": "success",
                    "message": "Update comment successfully.",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {
                "status": "failed",
                "message": "Updation failed.",
                "details": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request):
        comment_obj, error_response = self._get_comment(request)
        if error_response:
            return error_response

        comment_obj.archived = True
        comment_obj.save(update_fields=["archived"])
        return Response(
            {"status": "success", "message": "Comment deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )
