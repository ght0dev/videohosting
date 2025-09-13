from django.db import models

class Video(models.Model):
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    video_file = models.FileField(upload_to='videos/')
    created_at = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    comments = models.TextField(max_length=255, null=True, blank=True)
    