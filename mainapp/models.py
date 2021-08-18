from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.deletion import CASCADE
from django.http.response import HttpResponseRedirect
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.http import Http404
from django.contrib.auth.hashers import make_password
from mpesa_api.views import lipa_na_mpesa_online, call_back
from django.contrib import messages
from django.shortcuts import redirect
<<<<<<< HEAD
from mpesa_api.models import Payment
import time
=======
from djmoney.models.fields import MoneyField


>>>>>>> master

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
    location = models.CharField(max_length=200, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    nok_fullname = models.CharField(max_length=100, blank=True, null=True)
    nok_email = models.EmailField(blank=True, null=True)
    nok_number = models.CharField(max_length=100, blank=True, null=True)
    nok_relationship = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self) :
        return str(self.user.name)

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

class Unit(models.Model):
    name = models.CharField(max_length=200)
    width = models.PositiveIntegerField()
    height = models.PositiveIntegerField()
    length = models.PositiveIntegerField()
    occupied = models.BooleanField(default=False, null=True)
    daily_charge = MoneyField(max_digits=14, decimal_places=2, default_currency='KES')
    weekly_charge = MoneyField(max_digits=14, decimal_places=2, default_currency='KES')
    monthly_charge = MoneyField(max_digits=14, decimal_places=2, default_currency='KES')
    suitable_property =models.CharField(max_length=400)
    average_temperature = models.IntegerField()

    @property
    def volume(self):
        return self.width * self.length * self.height

    @property
    def size(self):
        if self.volume:
            if self.volume in range(1,1000):
                return 'Small'
            elif self.volume in range(1000, 2000):
                return 'Medium'
            elif self.volume in range(2000, 3000):
                return 'Large'
            elif self.volume in range(3000, 4000):
                return 'X-Large'
            elif self.volume in range(4000, 6000):
                return '2X-Large'
            elif self.volume in range(6000, 8000):
                return '3X-Large'

    def __str__(self):
        return self.name


    def save_unit(self):
        self.save()

    @classmethod
    def delete_unit(cls, unit_name):
        cls.objects.filter(name=unit_name).delete()

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
        units = Unit.objects.filter(name__icontains=search_term)
        return units

BillingCycle = (
    ('-----','-----'),
    ('Daily', 'Daily'),
    ('Weekly', 'Weekly'),
    ('Monthly', 'Monthly'),
)


ModePayment = (
    ('-----','-----'),
    ('Mpesa','Mpesa'),
    ('Bank', 'Bank'),
    ('Cash','Cash'),
)

class Booking(models.Model):
    profile = models.ForeignKey(Profile, related_name='profile', on_delete=CASCADE)
    unit = models.ForeignKey(Unit, related_name='unit', on_delete=CASCADE)
    description = models.CharField(max_length=200)
    start_date = models.DateTimeField(auto_now=True)
    end_date = models.DateTimeField(null=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    pickup = models.BooleanField(default=False, null=True, blank=True)
    delivery = models.BooleanField(default=False, null=True, blank=True)
    delivery_address = models.TextField(null=True, blank=True)
    billing_Cycle = models.CharField(max_length=100, choices=BillingCycle, default='-----')
    payment_mode = models.CharField(max_length=50, choices=ModePayment, default='-----')
    account_number = models.CharField(max_length=50, null=True, blank=True)
    access_code = models.PositiveIntegerField(default=0000)
    cost = MoneyField(max_digits=14, decimal_places=2, default_currency='KES')
    total_cost = MoneyField(max_digits=14, decimal_places=2, default_currency='KES')

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

    @classmethod
    def lipa_booking(cls, request, unitId, accountNumber, paymentMode):
        unit = Unit.objects.get(id=unitId)
        phonenumber = None

            
        if paymentMode == 'Mpesa':
            if accountNumber[0] == '0':
                phonenumber = '254'+ accountNumber[1:]
            elif accountNumber[0:2] == '254':
                phonenumber = accountNumber
            else:
                messages.error(request, 'Check you Phone Number format 2547xxxxxxxx')
                return redirect(request.get_full_path())

            messages.success(request, 'Your Payment is Being Proccessed')

            lipa_na_mpesa_online(request, phonenumber)

            time.sleep(27)

            latesttrans = Payment.objects.filter(phoneNumber=phonenumber).first() # get latest transcation

            if latesttrans:        
                Unit.objects.filter(id=unitId).update(occupied=True)
                messages.success(request, f'You Have Booked Unit {unit}')
            else:
                messages.error(request, 'Transaction Failed')
                return redirect(request.get_full_path())
        
        else:
            time.sleep(10)
            Unit.objects.filter(id=unitId).update(occupied=True)
            messages.success(request, f'You Have Booked Unit {unit}')
            