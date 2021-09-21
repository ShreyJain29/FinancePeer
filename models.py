from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
# Create your models here.
class User(AbstractUser):
    first_name = models.CharField(max_length=15, blank=True, null=True)
    last_name = models.CharField(max_length=15, blank=True, null=True)
    username = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']

    def __str__(self):
        return f"{self.first_name}"


class Filemodel(models.Model):
    Fuser = models.ForeignKey(User,on_delete=models.CASCADE, related_name='user_filedata')
    Title = models.CharField(max_length=250, blank=True, null=True)
    Body = models.CharField(max_length=500, blank=True, null=True)


class fileupload(models.Model):
    upload = models.FileField(upload_to=f'uploads/',
                              validators=[FileExtensionValidator(allowed_extensions=['json'])])

    def __str__(self):
        return f"{self.upload}"
