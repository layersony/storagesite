from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from mainapp.models import Profile
      
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=['pic','user','phone_number','address','nok_fullname','nok_number','nok_email','nok_relationship ']