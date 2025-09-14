from django.db import models

class Playlist(models.Model):
    name = models.CharField(max_length=255)
    videos = models.ManyToManyField('video.Video')
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name