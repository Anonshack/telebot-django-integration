from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import BotUsers, FeedbackForAdmin
from .serializers import (
    BotUsersSerializer,
    FeedbackSerializer,
    FeedbackCreateSerializer
)


class BotUsersListCreate(APIView):
    @swagger_auto_schema(
        operation_summary="List all bot users",
        responses={200: BotUsersSerializer(many=True)}
    )
    def get(self, request):
        users = BotUsers.objects.all().order_by("-created_at")
        result = []
        for user in users:
            result.append({
                "id": user.id,
                "user_id": user.user_id,
                "name": user.name,
                "username": user.username,
                "clean_username": user.clean_username,
                "full_info": user.get_info(),
                "created_at": user.created_at
            })
        return Response(result)

    @swagger_auto_schema(
        operation_summary="Create a new bot user",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["user_id"],
            properties={
                "user_id": openapi.Schema(type=openapi.TYPE_STRING, description="Unique Telegram User ID", example="123456789"),
                "name": openapi.Schema(type=openapi.TYPE_STRING, description="Full Name", example="Qudratbekh"),
                "username": openapi.Schema(type=openapi.TYPE_STRING, description="Telegram Username", example="geodev_at"),
            },
        ),
        responses={
            201: openapi.Response(description="Created user", schema=BotUsersSerializer()),
            400: "User already exists or invalid data"
        }
    )
    def post(self, request):
        user_id = request.data.get("user_id")
        if BotUsers.objects.filter(user_id=user_id).exists():
            return Response({"error": "This user already exists!"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = BotUsersSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "id": user.id,
                "user_id": user.user_id,
                "name": user.name,
                "username": user.username,
                "clean_username": user.clean_username,
                "full_info": user.get_info(),
                "created_at": user.created_at
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BotUsersDetail(APIView):
    def get_object(self, pk):
        try:
            return BotUsers.objects.get(pk=pk)
        except BotUsers.DoesNotExist:
            return None

    @swagger_auto_schema(
        operation_summary="Retrieve a bot user by ID",
        responses={200: BotUsersSerializer()}
    )
    def get(self, request, pk):
        user = self.get_object(pk)
        if not user:
            return Response({"error": "User not found"}, status=404)

        return Response({
            "id": user.id,
            "user_id": user.user_id,
            "name": user.name,
            "username": user.username,
            "clean_username": user.clean_username,
            "full_info": user.get_info(),
            "created_at": user.created_at
        })

    @swagger_auto_schema(
        operation_summary="Update a bot user",
        request_body=BotUsersSerializer,
        responses={200: BotUsersSerializer(), 400: "Invalid data"}
    )
    def put(self, request, pk):
        user = self.get_object(pk)
        if not user:
            return Response({"error": "User not found"}, status=404)

        serializer = BotUsersSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "id": user.id,
                "user_id": user.user_id,
                "name": user.name,
                "username": user.username,
                "clean_username": user.clean_username,
                "full_info": user.get_info(),
                "created_at": user.created_at
            })
        return Response(serializer.errors, status=400)

    @swagger_auto_schema(
        operation_summary="Delete a bot user",
        responses={204: "User deleted"}
    )
    def delete(self, request, pk):
        user = self.get_object(pk)
        if not user:
            return Response({"error": "User not found"}, status=404)

        user.delete()
        return Response(status=204)


class FeedbackListCreate(APIView):
    @swagger_auto_schema(
        operation_summary="List all feedbacks",
        responses={200: FeedbackSerializer(many=True)}
    )
    def get(self, request):
        feedbacks = FeedbackForAdmin.objects.all().order_by("-created_at")
        result = []
        for fb in feedbacks:
            result.append({
                "id": fb.id,
                "user": fb.user.id,
                "user_info": fb.user.get_info(),
                "text": fb.text,
                "created_at": fb.created_at
            })
        return Response(result)

    @swagger_auto_schema(
        operation_summary="Create a new feedback",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["user", "text"],
            properties={
                "user": openapi.Schema(type=openapi.TYPE_INTEGER, description="User ID", example=1),
                "text": openapi.Schema(type=openapi.TYPE_STRING, description="Feedback message", example="This is a feedback message.")
            }
        ),
        responses={201: FeedbackSerializer(), 400: "User does not exist or invalid data"}
    )
    def post(self, request):
        serializer = FeedbackCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data.get("user")
            if not BotUsers.objects.filter(id=user.id).exists():
                return Response({"error": "User does not exist!"}, status=status.HTTP_400_BAD_REQUEST)
            fb = serializer.save()
            return Response({
                "id": fb.id,
                "user": fb.user.id,
                "user_info": fb.user.get_info(),
                "text": fb.text,
                "created_at": fb.created_at
            }, status=201)
        return Response(serializer.errors, status=400)


class FeedbackDetail(APIView):
    def get_object(self, pk):
        try:
            return FeedbackForAdmin.objects.get(pk=pk)
        except FeedbackForAdmin.DoesNotExist:
            return None

    @swagger_auto_schema(
        operation_summary="Retrieve a feedback by ID",
        responses={200: FeedbackSerializer(), 404: "Feedback not found"}
    )
    def get(self, request, pk):
        fb = self.get_object(pk)
        if not fb:
            return Response({"error": "No Feedback!"}, status=404)

        return Response({
            "id": fb.id,
            "user": fb.user.id,
            "user_info": fb.user.get_info(),
            "text": fb.text,
            "created_at": fb.created_at
        })

    @swagger_auto_schema(
        operation_summary="Delete a feedback",
        responses={204: "Feedback deleted"}
    )
    def delete(self, request, pk):
        fb = self.get_object(pk)
        if not fb:
            return Response({"error": "No Feedback!"}, status=404)

        fb.delete()
        return Response(status=204)

    @swagger_auto_schema(
        operation_summary="Update a feedback",
        request_body=FeedbackCreateSerializer,
        responses={200: FeedbackSerializer(), 400: "Invalid data"}
    )
    def put(self, request, pk):
        fb = self.get_object(pk)
        if not fb:
            return Response({"error": "No Feedback!"}, status=404)

        serializer = FeedbackCreateSerializer(fb, data=request.data, partial=True)
        if serializer.is_valid():
            fb = serializer.save()
            return Response({
                "id": fb.id,
                "user": fb.user.id,
                "user_info": fb.user.get_info(),
                "text": fb.text,
                "created_at": fb.created_at
            })
        return Response(serializer.errors, status=400)
