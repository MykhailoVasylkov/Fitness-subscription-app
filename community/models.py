from django.db import models
from django.contrib.auth.models import User

class CommunityMessage(models.Model):
    user = models.CharField(max_length=100, default="Anonymous")
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    avatar = models.URLField(default='/media/avatars/default_avatar.jpg')

    def __str__(self):
        return f"{self.user}: {self.message[:10]}"

class CommunityPost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    body = models.TextField()
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    approved = models.BooleanField(default=True)
    
    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return f"Post by {self.author.username}"