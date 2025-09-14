from rest_framework import serializers
from .models import *
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']
        
class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ["id", "owner", "title", "description", "video_file", "thumbnail",
            "created_at", "views", "is_public", "is_blocked", "tags",
            "processing_status", "resolution", "duration", "slug"]
        
class VideoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ["title", "description", "video_file", "thumbnail", "tags", "is_public"]
    def create(self, validated_data):
        user = self.context["request"].user
        video = Video.objects.create(owner=user, **validated_data)
        return video      

class LikesDislaikesSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikesDislaikes
        fields = ["id", "video", "user", "is_like"]
        read_only_fields = ["user"]