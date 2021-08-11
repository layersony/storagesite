from django.http import JsonResponse
from django.shortcuts import render ,redirect,get_object_or_404
from django.http import HttpResponseRedirect
from .forms import BookingForm,PaymentForm, UpdateUserForm


from .models import User ,Profile,Booking,Unit
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

def update_profile(request):
    user = request.user

    if request.method == 'POST':
        userform = UpdateUserForm(request.POST, instance=request.user)
        form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid() and userform.is_valid():
            form.save()
            userform.save()
            return redirect('profile')
    else:
      userform = UpdateUserForm(instance=request.user)
      form = UpdateProfileForm(instance=request.user.profile)
    return render(request, 'all_customer/update_profile.html', { 'form': form, 'userform': userform})

def profile(request):
      units = Booking.objects.filter(profile=request.user.profile)
      return render(request, 'all_customer/profile.html', {'details':units})
    
def booking_details(request, id):
      book = Booking.objects.get(id=id)
      return render(request, 'all_customer/bookingdetails.html', {'book':book})

def available(request):
      units=Unit.objects.all()
      return render(request, 'all_customer/available_units.html', {"units":units})


def book(request):
      return render(request, 'all_customer/book.html', )

def book(request, pk):
      if pk:
            unit=Unit.objects.get(pk=pk)
      else:
            unit = request.user
      
      form_class = BookingForm()
      form = BookingForm()

      if request.method == 'POST':
            form = BookingForm(request.POST)
            if form.is_valid():
                  form.save()

      context = {'form': form}
      return render(request, 'all_customer/book.html',  context)


def payment(request):
      form_class = PaymentForm()
      form = PaymentForm()

      if request.method == 'POST':
            form = PaymentForm(request.POST)
            if form.is_valid():
                  form.save()

      context = {'form': form}
      return render(request, 'all_customer/payment.html', context)

def checkout(request):
      print(request.GET)
      data = {

      }
      return JsonResponse(data)
      
      
