from django.urls import path, include

urlpatterns = [
    path("users/", include("users.urls")),
    path("videos/", include("video.urls")),
    path("channels/", include("channels.urls")),
]
