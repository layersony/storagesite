from django.shortcuts import render , redirect,get_object_or_404
from django.http import HttpResponse

def index(request):
  return HttpResponse('Am Employee')

def units(request):
  return render (request,'units.html')

def onsite(request):
  return render (request,'onsite.html')

