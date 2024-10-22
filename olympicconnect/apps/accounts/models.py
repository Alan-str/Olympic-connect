import random
import string
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)
    security_key = models.CharField(max_length=150, unique=True, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def save(self, *args, **kwargs):
        if not self.security_key:
            self.security_key = self.generate_unique_security_key()
        super().save(*args, **kwargs)

    def generate_unique_security_key(self):
        length = 7
        characters = string.ascii_letters + string.digits
        while True:
            key = ''.join(random.choice(characters) for _ in range(length))
            if not CustomUser.objects.filter(security_key=key).exists():
                return key

    def __str__(self):
        return self.email
