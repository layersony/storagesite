from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.db.models.deletion import CASCADE
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save
from mainapp.models import Profile
from mainapp.models import Booking
from mainapp.models import Unit
from mainapp.models import User
from django.utils import timezone

# Create your models here.

