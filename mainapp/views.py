<<<<<<< HEAD
from django.http.response import Http404
from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, authenticate
from rest_framework import permissions, serializers
from .forms import RegistrationForm
from django.contrib import messages
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Booking
from .serializer import BookingSerializer
from rest_framework import status
from .permissions import IsAuthenticatedOrReadOnly
=======
from django.db.models.query_utils import select_related_descend
from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, authenticate
from .forms import RegistrationForm, AddUserForm, AddProfileForm, AddUnitForm, AddBookingForm
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import UnitSerializer
from .models import Unit, User, Profile, Booking
from rest_framework import status
from django.http import Http404
import hashlib
from rest_framework.permissions import IsAuthenticated, IsAdminUser
>>>>>>> master

def index(request):
  return render(request, 'index.html')

def signup(request):

  if request.method == 'POST':
    form = RegistrationForm(request.POST)
    if form.is_valid():
      temail = request.POST.get('email')
      password = request.POST.get('password1')
      clientname = form.cleaned_data.get('username')
      messages.success(request, 'Account was created for ' + clientname)

      regform = form.save(commit=False)
      regform.user_type='client'
      regform.save()

      user = authenticate(request, email=temail, password=password)

      if user is not None:
          login(request, user) 
          if user.is_authenticated and (user.user_type=='client'):
              return redirect('custhome')

      return redirect('home')

    else:
      messages.info(request, 'Error Processing Your Request')
      params = {
        'form': form
      }
      return render(request, 'registration/register.html', params)

  form = RegistrationForm()
  params = {
    'form' : form
  }
  return render(request, 'registration/register.html', params)

def sign_in(request):
  if request.method == 'POST':
      email = request.POST.get('email') 
      password = request.POST.get('password')

      user = authenticate(request, email=email, password=password)
      if user is not None:
          login(request, user)
          if user.is_authenticated and user.is_superuser:
            return redirect('customadmin')
          elif user.is_authenticated and (user.user_type=='employee'):
            return redirect('emphome') 
          elif user.is_authenticated and (user.user_type=='client'):
            return redirect('custhome')
      else:
        messages.info(request, 'Username Or Password is incorrect')
        return redirect('login')
  return render(request, 'registration/login.html')

def logout_user(request):
  logout(request)
  return redirect('home')


# Bookings API
class BookingList(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request, format=None):
        all_bookings = Booking.objects.all()
        serializers = BookingSerializer(all_bookings, many=True)
        return Response(serializers.data)

    def post(self, request, format=None):
        serializers = BookingSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

class BookingItem(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_booking(self, booking_id):
        try:
            return Booking.objects.get(pk=booking_id)
        except Booking.DoesNotExist:
            return Http404

    def get(self, request, booking_id, format=None):
        booking = self.get_booking(booking_id)
        serializers = BookingSerializer(booking)
        return Response(serializers.data)

    def put(self, request, booking_id, format=None):
        booking = self.get_booking(booking_id)
        serializers = BookingSerializer(booking, request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, booking_id, format=None):
        booking = self.get_booking(booking_id)
        booking.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
def customadmin(request):
  if request.method == 'POST':
    adduser = AddUserForm(request.POST or None, instance=request.user)
    addpro = AddProfileForm(request.POST or None, instance=request.user)
    addunit = AddUnitForm(request.POST)
    addbook = AddBookingForm(request.POST)
    print(request.POST)

    if adduser.is_valid():
      adduser.save()
      messages.success(request, 'User Added successfully')

    if addpro.is_valid():
      addpro.save()
      messages.success(request, 'Profile Added successfully')

    if addunit.is_valid():
      addunit.save()
      messages.success(request, 'Unit Added successfully')

    if addbook.is_valid():
      addbook.save()
      messages.success(request, 'Booking Added successfully')


  allusers = User.objects.all()
  allprofiles = Profile.objects.all()
  allunits = Unit.objects.all()
  allBooking = Booking.objects.all()

  available_units = Unit.objects.filter(occupied=False)
  occupied_units = Unit.objects.filter(occupied=True)

  adduser = AddUserForm()
  addpro = AddProfileForm()
  addunit = AddUnitForm()
  addbook = AddBookingForm()

  params = {
    'allusers':allusers,
    'allprofiles':allprofiles,
    'allunits':allunits,
    'allBooking':allBooking,
    'available_units':available_units,
    'occupied_units':occupied_units,
    'adduser':adduser,
    'addpro':addpro,
    'addunit':addunit,
    'addbook':addbook,
  }
  return render(request, 'customadmin/index.html', params)

def mainadminpost(request):
  if request.method == 'POST':
    adduser = AddUserForm(request.POST or None)
    addpro = AddProfileForm(request.POST or None)
    addunit = AddUnitForm(request.POST)
    addbook = AddBookingForm(request.POST)
    print(request.POST)

    if adduser.is_valid():
      adduser.save()
      messages.success(request, 'User Added successfully')
      return redirect('customadmin')

    if addpro.is_valid():
      addpro.save()
      messages.success(request, 'Profile Added successfully')
      return redirect('customadmin')

    if addunit.is_valid():
      addunit.save()
      messages.success(request, 'Unit Added successfully')
      return redirect('customadmin')

    if addbook.is_valid():
      addbook.save()
      messages.success(request, 'Booking Added successfully')
      return redirect('customadmin')

class AllUnits(APIView):
  permission_classes = (IsAuthenticated,)
  def get(self, request, format=None):
    allunits = Unit.objects.all()
    serializer = UnitSerializer(allunits, many=True)
    return Response(serializer.data)

  def post(self, request, format=None):
    serializer = UnitSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      # print(hashlib.md5(serializer.data['access_code']).hexdigest())
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OneUnit(APIView):
  permission_classes = (IsAuthenticated,)
  def get(self, request, id, format=None):
    one_unit = Unit.view_one_unit(id)
    serializer = UnitSerializer(one_unit, many=False)
    return Response(serializer.data)

  def put(self, request, id, format=None):
    one_unit = Unit.view_one_unit(id)
    serializers = UnitSerializer(one_unit, request.data)
    if serializers.is_valid():
        serializers.save()
        return Response(serializers.data)
    else:
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

  def delete(self, request, id, format=None):
    one_unit = Unit.view_one_unit(id)
    one_unit.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
