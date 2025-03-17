from django.db import models
from django.contrib.auth.models import AbstractUser

class Organisation(models.Model):
    org_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name
    
class User(AbstractUser):
    username = None
    email = models.EmailField('email', unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    profile_picture = models.URLField(max_length=256, blank=True, null=True)
    organisation = models.ForeignKey(Organisation, on_delete=models.SET_NULL, null=True, blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email



