from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db.models.base import Model
from .models import User ,Profile,Booking,Unit
from mainapp.views import AddProfileForm

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        exclude = ['unit', 'profile','end_date','delivery','delivery_address', 'access_code', 'cost','total_cost']   


class AddUserForm(forms.ModelForm):
    password1 = forms.CharField(label = "Password", required=True, widget=forms.TextInput(attrs={'placeholder':'Password', 'class': 'form-control', 'type':'password'}))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'name', 'password1']
