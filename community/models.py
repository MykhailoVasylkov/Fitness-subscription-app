from django.db import models

class CommunityMessage(models.Model):
    user = models.CharField(max_length=100, default="Anonymous")
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    avatar = models.URLField(default='/media/avatars/default_avatar.jpg')

    def __str__(self):
        return f"{self.user}: {self.message[:10]}"
