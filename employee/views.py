from django.shortcuts import render
from django.http import HttpResponse

def index(request):
  return HttpResponse('Am Employee')

def units(request):
  return(request,'units.html')

