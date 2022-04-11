from django.db import models
from map.models import Marker


class Event(models.Model):
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=300)
    location = models.ForeignKey(map.Marker, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Input(models.Model):
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.text[:50] + '...'
