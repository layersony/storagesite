from mpesa_api.models import Payment
from django.http.response import Http404
from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, authenticate
from rest_framework import permissions, serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import BookingSerializer, UnitSerializer, MyAuthTokenSerializer
from rest_framework import status
from .permissions import IsAuthenticatedOrReadOnly
from django.db.models.query_utils import select_related_descend
from .forms import RegistrationForm, AddUserForm, AddProfileForm, AddUnitForm, AddBookingForm
from django.contrib import messages
from .models import Unit, User, Profile, Booking
import hashlib
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authtoken import views as auth_views
from rest_framework.compat import coreapi, coreschema
from rest_framework.schemas import ManualSchema
from django.contrib.auth.decorators import login_required
from .emails import send_feedback


def index(request):
  return render(request, 'index.html')

def about(request):
  return render(request, 'about.html')

def contact(request):
    if request.method == 'POST':
        f_name = request.POST.get('f_name')
        l_name = request.POST.get('l_name')
        full_name = f_name + " " + l_name
        email = request.POST.get('email')
        message = request.POST.get('message')

        send_feedback(full_name, message, email)
        messages.success(request, 'Feedback sent successfully.')
        
    return render(request, 'contact.html')



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
              return redirect('profile')

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
      print(user)
      if user is not None:
          login(request, user)
          if user.is_authenticated and user.is_superuser:
            return redirect('customadmin')
          elif user.is_authenticated and (user.user_type=='employee'):
            return redirect('units') 
          elif user.is_authenticated and (user.user_type=='client'):
            return redirect('profile')
      else:
        messages.info(request, 'Username Or Password is incorrect')
        return redirect('login')
  return render(request, 'registration/login.html')

def logout_user(request):
  logout(request)
  return redirect('home')


# Bookings API
class MyAuthToken(auth_views.ObtainAuthToken):
    serializer_class = MyAuthTokenSerializer
    if coreapi is not None and coreschema is not None:
        schema = ManualSchema(
            fields=[
                coreapi.Field(
                    name="email",
                    required=True,
                    location='form',
                    schema=coreschema.String(
                        title="Email",
                        description="Valid email for authentication",
                    ),
                ),
                coreapi.Field(
                    name="password",
                    required=True,
                    location='form',
                    schema=coreschema.String(
                        title="Password",
                        description="Valid password for authentication",
                    ),
                ),
            ],
            encoding="application/json",
        )

obtain_auth_token = MyAuthToken.as_view()

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
        messages.success(request, 'Delated successfully')
        return Response(status=status.HTTP_204_NO_CONTENT)

@login_required(login_url='login')
def customadmin(request):
  if request.user.is_superuser:
    if request.method == 'POST':
      adduser = AddUserForm(request.POST or None)
      addpro = AddProfileForm(request.POST or None, request.FILES)
      addunit = AddUnitForm(request.POST)
      addbook = AddBookingForm(request.POST)

      if adduser.is_valid():
        add_user = adduser.save(commit=False)
        add_user.set_password(adduser.cleaned_data['password1'])
        add_user.save()
        messages.success(request, 'User Added successfully')

      if addpro.is_valid():
        addpro.save()
        messages.success(request, 'Profile Added successfully')

      if addunit.is_valid():
        addunit.save()
        messages.success(request, 'Unit Added successfully')

      if addbook.is_valid():      
        if Unit.objects.get(id=addbook.cleaned_data['unit'].id).occupied == False:
          accountnumber = addbook.cleaned_data['account_number']
          payment = addbook.cleaned_data['payment_mode']
          Booking.lipa_booking(request, addbook.cleaned_data['unit'].id, accountnumber, payment)
          Unit.objects.filter(id=addbook.cleaned_data['unit'].id).update(occupied=True)
          addbook.save()
          messages.success(request, 'Booking Added successfully')
          return redirect('customadmin')
        else:
          messages.error(request, f'Sorry {addbook.cleaned_data["unit"]} Has Already Being Booked')

    allusers = User.objects.all()
    allprofiles = Profile.objects.all()
    allunits = Unit.objects.all()
    allBooking = Booking.objects.all()
    allPayments = Payment.objects.all()

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
      'allPayments':allPayments,
    }
    return render(request, 'customadmin/index.html', params)
  else:
    messages.error(request, f'You are not Authorized to Access the Admin Page')
    return redirect('home')

@login_required(login_url='login')
def mainadminupdateuser(request, id):
  userto = User.objects.get(id=id)
  if request.method == 'POST':
    adduser = AddUserForm(request.POST, instance=userto)
    if adduser.is_valid():
      add_user = adduser.save(commit=False)
      add_user.set_password(adduser.cleaned_data['password1'])
      add_user.save()
      return redirect('customadmin')
  
  adduser = AddUserForm(instance=userto)
  params = {
    'adduser':adduser,
    'userto':userto
  }
  return render(request, 'customadmin/update.html', params)

@login_required(login_url='login')
def deleteuser(request, id):
  userto = User.objects.get(id=id)
  if request.method == 'POST':
    userto.delete()
    messages.success(request, 'Delated successfully')
    return redirect('customadmin')

@login_required(login_url='login')
def mainadminupdateprofile(request, id):
  userto = Profile.objects.get(id=id)
  if request.method == 'POST':
    addpro = AddProfileForm(request.POST, instance=userto)
    if addpro.is_valid():
      addpro.save()
      return redirect('customadmin')
  
  addpro = AddProfileForm(instance=userto)
  params = {
    'addpro':addpro,
    'userto':userto
  }
  return render(request, 'customadmin/updateprofile.html', params)

@login_required(login_url='login')
def deleteprofile(request, id):
  userto = Profile.objects.get(id=id)
  if request.method == 'POST':
    userto.delete()
    messages.success(request, 'Delated successfully')
    return redirect('customadmin')

@login_required(login_url='login')
def mainadminupdateunit(request, id):
  unit = Unit.objects.get(id=id)
  if request.method == 'POST':
    addunit = AddUnitForm(request.POST, instance=unit)
    if addunit.is_valid():
      addunit.save()
      messages.success(request, 'Updated successfully')
      return redirect('customadmin')
  
  addunit = AddUnitForm(instance=unit)
  params = {
    'addunit':addunit,
    'unit':unit
  }
  return render(request, 'customadmin/updateunit.html', params)

@login_required(login_url='login')
def deleteunit(request, id):
  unit = Unit.objects.get(id=id)
  if request.method == 'POST':
    unit.delete()
    messages.success(request, 'Delated successfully')
    return redirect('customadmin')

@login_required(login_url='login')
def mainadminupdatebook(request, id):
  book = Booking.objects.get(id=id)
  if request.method == 'POST':

    addbook = AddBookingForm(request.POST or None, instance=book)

    if 'update' in request.POST and addbook.is_valid():
      addbook.save()
      print('redirecting')
      return redirect('customadmin')
    if 'delete' in request.POST:
      print(request.POST)
  

  addbook = AddBookingForm(instance=book)
  params = {
    'addbook':addbook,
    'book':book
  }
  return render(request, 'customadmin/updatebook.html', params)

@login_required(login_url='login')
def deletebook(request, id):
  book = Booking.objects.get(id=id)
  if request.method == 'POST':
    book.delete()
    Unit.objects.filter(id=book.unit.id).update(occupied=False)
    messages.success(request, f'{book} Deleted Successfully')
    return redirect('customadmin')

class AllUnits(APIView):
  permission_classes = (IsAuthenticatedOrReadOnly,)
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
    messages.success(request, 'Delated successfully')
    return Response(status=status.HTTP_204_NO_CONTENT)
