from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


class UserProfile(models.Model):                # <all 5
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    last_activity = models.DateTimeField(default=timezone.now)

    def is_online(self):
        if self.last_activity:
            return timezone.now() - self.last_activity < timedelta(minutes=5)
        return False

    def __str__(self):
        return self.user.username
