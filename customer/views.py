from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages

from .forms import UpdateProfileForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from mainapp.models import Profile, User
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView


from . import views
from django.conf import settings

# def updateProfile(request):
#     user = request.user
#     if request.method == 'POST':
#         form = UpdateProfileForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('all_customer/profile', user.username)
#     else:
#         form = UpdateProfileForm()
#     return render(request, 'all_customer/updateProfile.html', {'form': form})


class ProfileUpdate(UpdateView):
    model = Profile
    fields = '__all__'
    template_name = 'all_customer/update_profile.html'
    
    def get_object(self):
        return self.request.user.profile
    
class Profile(DetailView):
    template_name = 'all_customer/profile.html'
    
    def get_object(self):
        return self.request.user.profile
                

def bookingDetails(request):
    return render(request, 'all_customer/booking_details.html')

def available(request):
      return render(request, 'all_customer/available_units.html', )

def book(request):
      return render(request, 'all_customer/book.html', )


def payment(request):
      return render(request, 'all_customer/payment.html', )
