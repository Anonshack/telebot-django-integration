from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import BotUsers, FeedbackForAdmin
from .serializers import (
    BotUsersSerializer,
    FeedbackSerializer,
    FeedbackCreateSerializer
)

class BotUsersListCreate(APIView):
    def get(self, request):
        users = BotUsers.objects.all().order_by("-created_at")
        serializer = BotUsersSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        user_id = request.data.get("user_id")

        if BotUsers.objects.filter(user_id=user_id).exists():
            return Response(
                {"error": "Bu user allaqachon mavjud."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = BotUsersSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BotUsersDetail(APIView):
    def get_object(self, pk):
        try:
            return BotUsers.objects.get(pk=pk)
        except BotUsers.DoesNotExist:
            return None

    def get(self, request, pk):
        user = self.get_object(pk)
        if not user:
            return Response({"error": "User topilmadi"}, status=404)

        serializer = BotUsersSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk):
        user = self.get_object(pk)
        if not user:
            return Response({"error": "User topilmadi"}, status=404)

        serializer = BotUsersSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        user = self.get_object(pk)
        if not user:
            return Response({"error": "User topilmadi"}, status=404)

        user.delete()
        return Response(status=204)


class FeedbackListCreate(APIView):
    def get(self, request):
        feedbacks = FeedbackForAdmin.objects.all().order_by("-created_at")
        serializer = FeedbackSerializer(feedbacks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = FeedbackCreateSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data.get("user")

            if not BotUsers.objects.filter(id=user.id).exists():
                return Response(
                    {"error": "Bunday user mavjud emas"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            serializer.save()
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)


class FeedbackDetail(APIView):
    def get_object(self, pk):
        try:
            return FeedbackForAdmin.objects.get(pk=pk)
        except FeedbackForAdmin.DoesNotExist:
            return None

    def get(self, request, pk):
        fb = self.get_object(pk)
        if not fb:
            return Response({"error": "Feedback topilmadi"}, status=404)

        serializer = FeedbackSerializer(fb)
        return Response(serializer.data)

    def delete(self, request, pk):
        fb = self.get_object(pk)
        if not fb:
            return Response({"error": "Feedback topilmadi"}, status=404)

        fb.delete()
        return Response(status=204)
