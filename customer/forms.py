from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
from .models import Booking
from mainapp.models import Profile
from django.contrib.auth.forms import UserCreationForm



class BookingForm(ModelForm):
    address = forms.CharField(label='Pick Up Address',widget=forms.Textarea(attrs={"rows":5, "cols":20}))
    account_number = forms.CharField(label='Account _Number',widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'...'}))
    pickup = forms.BooleanField(label='Pick Up (200 ksh)', widget=forms.CheckboxInput, required=True)
    class Meta:
        model = Booking
        fields = ['description','billing_Cycle', 'pickup', 'address', 'payment_mode','account_number']
        
        widgets = {
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'account_number': forms.TextInput(attrs={'class': 'form-control'}),
            'total_cost': forms.TextInput(attrs={'class': 'form-control'}),
        }


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['pic', 'phone_number','location','address', 'nok_fullname',
                  'nok_number', 'nok_email', 'nok_relationship',]
        
class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'
        exclude = ['user_type', 'is_staff', 'is_active', 'is_superuser', 'last_login', 'date_joined', 'groups', 'user_permissions', 'password']