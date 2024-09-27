from django.db import models

# Create your models here.
class Notification(models.Model):
    user = models.ForeignKey(
        "authentication.Account",
        on_delete=models.CASCADE,
        blank=False,
        null=False
    )
    title = models.CharField(max_length=256,)
    content = models.TextField(default='')
    url = models.CharField(max_length=256,)
    datetime = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)