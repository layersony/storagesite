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
  class Meta:
    model = User
    fields = '__all__'

class AddProfileForm(forms.ModelForm):
  class Meta:
    model = Profile
    fields = '__all__'

class AddUnitForm(forms.ModelForm):
  class Meta:
    model = Unit
    fields = '__all__'

class AddBookingForm(forms.ModelForm):
  class Meta:
    model = Booking
    fields = '__all__'