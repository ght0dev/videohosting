from django.db import models

class Channel(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE)
    subscribers = models.ManyToManyField('users.User', related_name='subscribed_channels')
    videos = models.ManyToManyField('video.Video', related_name='channels')
    current_video = models.ForeignKey('video.Video', on_delete=models.SET_NULL, null=True, blank=True, related_name='current_channel')
    channel_description = models.TextField(max_length=150, blank=True, null=True)
    
    