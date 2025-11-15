from rest_framework import serializers
from .models import BotUsers, FeedbackForAdmin

# bot users
class BotUsersSerializer(serializers.ModelSerializer):
    clean_username = serializers.CharField(read_only=True)  
    full_info = serializers.SerializerMethodField()

    class Meta:
        model = BotUsers
        fields = [
            "id",
            "user_id",
            "name",
            "username",
            "clean_username",
            "created_at",
            "full_info",
        ]
        read_only_fields = ("created_at",)

    def get_full_info(self, obj):
        return obj.get_info()


# feedback part
class FeedbackSerializer(serializers.ModelSerializer):
    user_info = serializers.SerializerMethodField()

    class Meta:
        model = FeedbackForAdmin
        fields = [
            "id",
            "user",
            "user_info",
            "text",
            "created_at",
        ]
        read_only_fields = ("created_at",)

    def get_user_info(self, obj):
        return {
            "user_id": obj.user.user_id,
            "name": obj.user.name,
            "username": obj.user.username,
        }


# feedback create serializer
class FeedbackCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedbackForAdmin
        fields = ["user", "text"]
