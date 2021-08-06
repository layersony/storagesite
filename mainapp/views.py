from django.db.models.query_utils import select_related_descend
from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, authenticate
from .forms import RegistrationForm
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import UnitSerializer
from .models import Unit
from rest_framework import status
from django.http import Http404
import hashlib
from rest_framework.permissions import IsAuthenticated, IsAdminUser

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
            return redirect('admin:index')
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
