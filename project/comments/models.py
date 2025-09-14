from django.db import models

# Create your models here.
class Comment(models.Model):
    video = models.ForeignKey('video.Video', on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} → {self.video}"
    
    