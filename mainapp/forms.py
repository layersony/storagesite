from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db.models.base import Model
from .models import User

class RegistrationForm(UserCreationForm):
  email = forms.EmailField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
  name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
  username = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
  password1 = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'type':'password'}))
  password2 = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'type':'password'}))

  class Meta:
    model = User
    fields = ['username', 'email', 'name', 'password1', 'password2']