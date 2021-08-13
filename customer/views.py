from django.http import JsonResponse
from django.shortcuts import render ,redirect,get_object_or_404
from django.http import HttpResponseRedirect
from .forms import BookingForm, UpdateUserForm


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
from django.contrib.auth.forms import UserCreationForm

from mpesa_api.views import lipa_na_mpesa_online

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
                  bkunit = form.save(commit=False)
                  bkunit.profile = request.user.profile
                  bkunit.unit = unit
                  bkunit.save()

                  account_number = form.cleaned_data['account_number']
                  payment = form.cleaned_data['payment_mode']

                  phonenumber = None
                  if account_number[0] == '0':
                      phonenumber = '254'+ account_number[1:]
                  
                  if payment == 'Mpesa':
                        lipa_na_mpesa_online(request, phonenumber)
                        messages.success(request, 'Your Payment is Being Proccessed')
                        Unit.objects.filter(name=pk).update(occupied=True)
                        messages.success(request, f'You Have Booked Unit {pk}')
                        return redirect('profile')

      context = {'form': form, "unit":unit}
      return render(request, 'all_customer/book.html',  context)

# @login_required
# def payment(request):
#       form_class = PaymentForm()
#       form = PaymentForm()

#       if request.method == 'POST':
#             form = PaymentForm(request.POST)
#             if form.is_valid():
#                   form.save()

#       context = {'form': form}
#       return render(request, 'all_customer/payment.html', context)

def checkout(request):
      unit_id = request.GET.get('unit')
      book_id = request.GET.get('booking')
      Unit.objects.filter(id=unit_id).update(occupied=False)
      Booking.delete_booking(book_id)
      message = messages.success(request ,f'You have Successfully Moved Out of unit {Unit.objects.get(id=unit_id).name}')
      data = {
            'message':message
      }
      return JsonResponse(data)
      
      



