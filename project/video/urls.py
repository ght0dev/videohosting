from django.urls import path
from .views import *

urlpatterns = [
    
    path("", VideoListView.as_view(), name="video-list"),
    path("upload/", VideoCreateView.as_view(), name="video-upload"),
    path("<slug:slug>/", VideoDetailView.as_view(), name="video-detail"),
    path('<int:pk>/like/', VideoLikeView.as_view(), name='video-like'),
    path('<int:pk>/dislike/', VideoDislikeView.as_view(), name='video-dislike'),

]