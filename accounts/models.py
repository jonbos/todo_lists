from django.db import models
from django.contrib import auth
import uuid
# Create your models here.

auth.signals.user_logged_in.disconnect(auth.models.update_last_login)
class User(models.Model):
    email = models.EmailField(primary_key=True)
    is_anonymous = False
    is_authenticated = True
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Token(models.Model):
    email = models.EmailField()
    uid = models.CharField(default=uuid.uuid4, max_length=40)
