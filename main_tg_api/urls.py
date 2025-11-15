from django.urls import path
from .views import (
    BotUsersListCreate,
    FeedbackListCreate,
)

urlpatterns = [
    path("users/", BotUsersListCreate.as_view(), name="users-list-create"),
    path("feedbacks/", FeedbackListCreate.as_view(), name="feedbacks-list-create"),
]
