from django.forms import ModelForm
from django import forms
from .models import Booking
from mainapp.models import Profile



class BookingForm(ModelForm):
    class Meta:
        model = Booking
        fields = ['description','address']

        widgets = {
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
        }


class PaymentForm(ModelForm):
    class Meta:
        model = Booking
        fields = ['payment_mode','account_number','total_cost']
        
        widgets = {
            'payment_mode': forms.TextInput(attrs={'class': 'form-control'}),
            'account_number': forms.TextInput(attrs={'class': 'form-control'}),
            'total_cost': forms.TextInput(attrs={'class': 'form-control'}),
        }

  


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('pic','user', 'phone_number', 'address', 'nok_fullname',
                  'nok_number', 'nok_email', 'nok_relationship',)
