from django.db import models
from django.contrib.auth.models import User

from api.shared.mixins import TimestampMixin


class ApiKey(TimestampMixin):
    key = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.key
