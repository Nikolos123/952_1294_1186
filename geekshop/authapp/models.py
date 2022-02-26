from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):

    image = models.ImageField(upload_to='users_images', blank=True)
    age = models.PositiveIntegerField(verbose_name='возраст', default=18)
