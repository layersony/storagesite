from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db.models.base import Model
from .models import User ,Profile,Booking,Unit


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields ='__all__'    
