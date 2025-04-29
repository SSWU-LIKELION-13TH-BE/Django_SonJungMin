from django.db import models
from django.conf import settings

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=20, blank=False, null=False)
    content = models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    TECH_STACK_CHOICES = (
        ('Python', 'Python'),
        ('Java', 'Java'),
        ('C++', 'C++'),
        ('ect', '그 외'),
    )
    techstack = models.CharField(max_length=7, default="ect", choices=TECH_STACK_CHOICES, verbose_name="사용한 기술 스택")
    githublink = models.CharField(max_length=100, blank=True, null=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_posts')
    views = models.IntegerField(default=0)
    
    def __str__(self):
        return self.title
    
class Image(models.Model):
    post=models.ForeignKey(Post, on_delete=models.CASCADE)
    image=models.ImageField(upload_to = 'images/', null=True, blank = True)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', null=True)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies', null=True, blank=True)
    comment_content = models.TextField()
    comment_datetime = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_comments')

    
    def __str__(self):
        return self.comment_content