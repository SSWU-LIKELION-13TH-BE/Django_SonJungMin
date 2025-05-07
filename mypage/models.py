from django.db import models
from user.models import CustomUser

# Create your models here.
class GuestBook(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='guestbook_received')
    writer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='guestbook_written')
    content = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)