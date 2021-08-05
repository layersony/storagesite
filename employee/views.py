from django.shortcuts import render 
from django.http import HttpResponse


def units(request):
  return render (request,'employee/units.html')


