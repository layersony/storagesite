from django.shortcuts import render
from django.http import HttpResponse

def index(request):
  return HttpResponse('Am Employee')

def employee(request):
  return render(request,'employee.html')
