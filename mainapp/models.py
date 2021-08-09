from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.deletion import CASCADE
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.http import Http404
from django.contrib.auth.hashers import make_password


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

User_Types = (
	('client', 'Client'),
	('employee', 'Employee'),
)

class User(AbstractBaseUser, PermissionsMixin):
	username = models.CharField(max_length=254, unique=True, null=True, blank=True)
	email = models.EmailField(max_length=254, unique=True)
	name = models.CharField(max_length=254, null=True, blank=True)
	user_type = models.CharField('User Type', choices=User_Types, null=True, blank=True,max_length=100)
	is_staff = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	last_login = models.DateTimeField(null=True, blank=True)
	date_joined = models.DateTimeField(auto_now_add=True)

	USERNAME_FIELD = 'email'
	EMAIL_FIELD = 'email'
	REQUIRED_FIELDS = []

	objects = UserManager()


	def get_email(self):
			return self.email

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    pic = models.ImageField(upload_to='profiles/', default='profiles/default.jpg')
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=20, blank=True, null=True)
    nok_fullname = models.CharField(max_length=100, blank=True, null=True)
    nok_email = models.EmailField(blank=True, null=True)
    nok_number = models.CharField(max_length=100, blank=True, null=True)
    nok_relationship = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self) :
        return str(self.user.username)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def save_user(self):
        self.save()

    @classmethod
    def delete_user(cls, id):
        cls.objects.filter(id=id).delete()

    @classmethod
    def update_user(cls, id, *args, **kwargs):
        cls.objects.filter(id=id).update(*args, **kwargs)
    
    def view_all(self):
        all_profiles = self.objects.all()
        return all_profiles

    def view_one_profile(self, id):
        one_profile = self.objects.filter(id=id)
        return one_profile

Unit_sizes = (
    ('-----','-----'),
    ('Small','Small'),
    ('Medium', 'Medium'),
    ('Large', 'Large'),
    ('X-large', 'X-large'),
    ('2X-large', '2X-large'),
    ('3X=large', '3X-large'),
)

class Unit(models.Model):
    name = models.CharField(max_length=200)
    width = models.PositiveIntegerField()
    height = models.PositiveIntegerField()
    length = models.PositiveIntegerField()
    size = models.CharField(max_length=100, choices=Unit_sizes, default='-----')
    occupied = models.BooleanField(default=False, null=True)
    daily_charge = models.PositiveIntegerField()
    weekly_charge = models.PositiveIntegerField()
    monthly_charge = models.PositiveIntegerField()
    access_code = models.PositiveIntegerField()

    def __str__(self):
        return self.name


    def save_unit(self):
        self.save()

    @classmethod
    def delete_unit(cls, id):
        cls.objects.filter(id=id).delete()

    @classmethod
    def update_unit(cls, id, *args, **kwargs):
        cls.objects.filter(id=id).update(*args, **kwargs)
    
    def view_all(self):
        allunits = self.objects.all()
        return allunits
    
    @classmethod
    def view_one_unit(cls, id):
        try:
            return cls.objects.get(pk=id)
        except Unit.DoesNotExist:
            return Http404
    
    @classmethod
    def search(cls,search_term):
        units = Unit.objects.filter(name__icontains=search_term).all()
        return units

class Booking(models.Model):
    profile = models.ForeignKey(Profile, related_name='profile', on_delete=CASCADE)
    unit = models.ForeignKey(Unit, related_name='unit', on_delete=CASCADE)

    description = models.CharField(max_length=200)
    start_date = models.DateTimeField(auto_now=True)
    end_date = models.DateTimeField(null=True)
    address = models.CharField(max_length=200)
    pickup = models.BooleanField(default=False)
    payment_mode = models.CharField(max_length=200)
    account_number = models.CharField(max_length=30)
    total_cost = models.PositiveIntegerField(null=True)

    def __str__(self) :
        return f'{self.unit.name} Booked By {self.profile.user.username}'

    def save_booking(self):
        self.save()

    @classmethod
    def delete_booking(cls, id):
        cls.objects.filter(id=id).delete()

    @classmethod
    def update_booking(cls, id, *args, **kwargs):
        cls.objects.filter(id=id).update(*args, **kwargs)
    
    def view_all_booking(self):
        allbookings = self.objects.all()
        return allbookings
    
    @classmethod
    def view_one_booking(cls, id):
        abooking = cls.objects.get(id=id)
        return abooking