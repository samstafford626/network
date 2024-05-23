from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    
    pass


# Posts

class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="posts")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField("User", related_name="liked_posts")
    @property
    def likes_count(self):
        return self.likes.count()