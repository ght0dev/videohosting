from django.db import models

class Subscription(models.Model):
    subscriber = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='user_subscriptions')
    channel = models.ForeignKey('channels.Channel', on_delete=models.CASCADE, related_name='channel_subscribers')
    created_at = models.DateTimeField(auto_now_add=True)