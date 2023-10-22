from django.db import models
from django.contrib.auth.models import User
from django.utils.text import Truncator
# Create your models here.

class Board(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(max_length=200)

    def __str__(self) -> str:
        return str(self.name)
    
    def get_posts_count(self):
        return Post.objects.filter(topic__board=self).count()

    def get_last_post(self):
        return Post.objects.filter(topic__board=self).order_by('-created_at').first()

class Topic(models.Model):
    subject = models.CharField(max_length=100)
    last_update = models.DateTimeField(auto_now_add=True)
    # related_name argument is used to create a 'reverse relationship'
    # The User instance will have access to a list of Topic instances that belong to it
    starter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='topics')
    # The Board instance will have access to a list of Topic instances that belong to it
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='topics')
    views = models.PositiveIntegerField(default=0) 

    def __str__(self) -> str:
        return str(self.subject)

class Post(models.Model):
    message = models.TextField(max_length=10000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    # The Topic instance will have access to a list of Post instances that belong to it
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='posts')
    # The User instance will have access to a list of Post instances that belong to it
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='+')

    def __str__(self):
        truncated_message = Truncator(self.message)
        return truncated_message.chars(30)
