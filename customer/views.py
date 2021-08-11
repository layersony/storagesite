from django.shortcuts import render ,redirect,get_object_or_404
from django.http import HttpResponseRedirect
from .forms import BookingForm,PaymentForm
from .models import User ,Profile,Booking,Unit
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from .forms import UpdateProfileForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from mainapp.models import Profile, User
from . import views
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm

def updateProfile(request):
    user = request.user
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('all_customer/profile', user.username)
    else:
        form = UpdateProfileForm()
    return render(request, 'all_customer/updateProfile.html', {'form': form})


def profile(request):
    return render(request, 'all_customer/profile.html')

@login_required
def available(request):
      units=Unit.objects.all()
      return render(request, 'all_customer/available_units.html', {"units":units})


@login_required
def book(request, pk):

      unit=Unit.objects.get(name=pk)
      

      form_class = BookingForm()
      form = BookingForm()

      if request.method == 'POST':
            form = BookingForm(request.POST)
            if form.is_valid():
                  form.save()

      context = {'form': form, "unit":unit}
      return render(request, 'all_customer/book.html',  context)

@login_required
def payment(request):
      form_class = PaymentForm()
      form = PaymentForm()

      if request.method == 'POST':
            form = PaymentForm(request.POST)
            if form.is_valid():
                  form.save()

      context = {'form': form}
      return render(request, 'all_customer/payment.html', context)




