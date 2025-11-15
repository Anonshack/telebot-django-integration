from django.urls import path
from .views import (
    BotUsersListCreate,
    BotUsersDetail,
    FeedbackListCreate,
    FeedbackDetail
)

urlpatterns = [
    path("users/", BotUsersListCreate.as_view(), name="users-list-create"),       # GET: list, POST: create
    path("users/<int:pk>/", BotUsersDetail.as_view(), name="users-detail"),       # GET: retrieve, PUT: update, DELETE: delete

    path("feedbacks/", FeedbackListCreate.as_view(), name="feedbacks-list-create"),  # GET: list, POST: create
    path("feedbacks/<int:pk>/", FeedbackDetail.as_view(), name="feedbacks-detail"),  # GET: retrieve, PUT: update, DELETE: delete
]
