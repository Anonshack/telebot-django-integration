from django.urls import path
from .views import (
    BotUsersListCreate, BotUsersDetail,
    FeedbackListCreate, FeedbackDetail
)

urlpatterns = [
    path("users/", BotUsersListCreate.as_view(), name="users-list-create"),
    path("users/<int:pk>/", BotUsersDetail.as_view(), name="users-detail"),

    path("feedbacks/", FeedbackListCreate.as_view(), name="feedbacks-list-create"),
    path("feedbacks/<int:pk>/", FeedbackDetail.as_view(), name="feedbacks-detail"),
]
