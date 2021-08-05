from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save

class UserManager(BaseUserManager):

    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            last_login=now,
            date_joined=now,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        user = self._create_user(email, password, True, True, **extra_fields)
        user.save(using=self._db)
        return user


class UserType(models.Model):
    # is_customer = models.BooleanField(default=False)
    # is_employee = models.BooleanField(default=False)
    # # user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_type_custom')

    # def __str__(self):
    #     if self.is_employee == True:
    #         return User.get_email(self.user) + " - is_employee"
    #     else:
    #         return User.get_email(self.user) + " - is_customer"

    role = models.CharField(max_length=100, blank=True, null=True)
            
    def __str__(self):
        return self.role
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=254, unique=True, null=True, blank=True)
    email = models.EmailField(max_length=254, unique=True)
    name = models.CharField(max_length=254, null=True, blank=True)
    user_type = models.ForeignKey(UserType, on_delete=models.CASCADE, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    # def get_absolute_url(self): # go to profile
    #     return "/users/%i/" % (self.pk)
    def get_email(self):
        return self.email

