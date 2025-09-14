from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Video
from .serializers import *

class VideoListView(generics.ListAPIView):
    queryset = Video.objects.filter(is_public=True, is_blocked=False).order_by("-created_at")
    serializer_class = VideoSerializer
    permission_classes = [permissions.AllowAny]
    
class VideoDetailView(generics.RetrieveAPIView):
    queryset = Video.objects.filter(is_public=True, is_blocked=False)
    serializer_class = VideoSerializer
    lookup_field = "slug"
    permission_classes = [permissions.AllowAny]
    
class VideoCreateView(generics.CreateAPIView):
    serializer_class = VideoCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        
class VideoLikeView(generics.GenericAPIView):
    serializer_class = LikesDislaikesSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        video = Video.objects.get(pk=pk)
        obj, created = LikesDislaikes.objects.get_or_create(user=request.user, video=video)
        obj.is_like = True
        obj.save()
        return Response({"detail": "Video liked"}, status=status.HTTP_200_OK)


class VideoDislikeView(generics.GenericAPIView):
    serializer_class = LikesDislaikesSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        video = Video.objects.get(pk=pk)
        obj, created = LikesDislaikes.objects.get_or_create(user=request.user, video=video)
        obj.is_like = False
        obj.save()
        return Response({"detail": "Video disliked"}, status=status.HTTP_200_OK)