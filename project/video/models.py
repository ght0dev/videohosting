from django.db import models
from django.utils.text import slugify

class Video(models.Model):
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='videos')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    video_file = models.FileField(upload_to='videos/')
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    views = models.PositiveIntegerField(default=0)
    likes_count = models.PositiveIntegerField(default=0)
    dislikes_count = models.PositiveIntegerField(default=0)

    is_public = models.BooleanField(default=True)
    is_blocked = models.BooleanField(default=False)

    tags = models.ManyToManyField('Tag', blank=True, related_name='videos')

    processing_status = models.CharField(
        max_length=20,
        choices=[("pending", "Pending"), ("processing", "Processing"),
                 ("done", "Done"), ("failed", "Failed")],
        default="pending"
    )
    resolution = models.CharField(max_length=50, default="1080p")
    duration = models.DurationField(null=True, blank=True)

    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class LikesDislaikes(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    is_like = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ("video", "user")
   
class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name