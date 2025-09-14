from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import *

@receiver(post_save, sender=LikesDislaikes)
def update_likes_dislikes_on_save(sender, instance, created, **kwargs):
    video = instance.video
    video.likes_count = LikesDislaikes.objects.filter(video=video, is_like=True).count()
    video.dislikes_count = LikesDislaikes.objects.filter(video=video, is_like=False).count()
    video.save(update_fields=['likes_count', 'dislikes_count'])


@receiver(post_delete, sender=LikesDislaikes)
def update_likes_dislikes_on_delete(sender, instance, **kwargs):
    video = instance.video
    video.likes_count = LikesDislaikes.objects.filter(video=video, is_like=True).count()
    video.dislikes_count = LikesDislaikes.objects.filter(video=video, is_like=False).count()
    video.save(update_fields=['likes_count', 'dislikes_count'])
