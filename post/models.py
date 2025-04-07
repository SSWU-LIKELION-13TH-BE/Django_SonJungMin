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
    
    
    
    def __str__(self):
        return self.title
    
class Image(models.Model):
    post=models.ForeignKey(Post, on_delete=models.CASCADE)
    image=models.ImageField(upload_to = 'images/', null=True, blank = True)

