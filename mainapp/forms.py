from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Booking, Profile, User, Unit

class RegistrationForm(UserCreationForm):
  email = forms.EmailField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
  name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
  username = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
  password1 = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'type':'password'}))
  password2 = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'type':'password'}))

  class Meta:
    model = User
    fields = ['username', 'email', 'name', 'password1', 'password2']

class AddUserForm(forms.ModelForm):
  password1 = forms.CharField(label = "Password", required=True, widget=forms.TextInput(attrs={'placeholder':'Password', 'class': 'form-control', 'type':'password'}))

  class Meta:
    model = User
    fields = ['username', 'email', 'name', 'user_type', 'is_staff', 'is_superuser', 'is_active', 'password1']
    

class AddProfileForm(forms.ModelForm):
  address = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Address', 'id':'profileaddress'}))
  class Meta:
    model = Profile
    fields = '__all__'

class AddUnitForm(forms.ModelForm):
  name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'UnitName', 'id':'unitname'}))
  class Meta:
    model = Unit
    fields = '__all__'

class AddBookingForm(forms.ModelForm):
  class Meta:
    model = Booking
    fields = '__all__'