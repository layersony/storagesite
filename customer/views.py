from django.shortcuts import render
from django.http import HttpResponse

def available(request):
      return render(request, 'all_customer/available_units.html', )


def book(request):
      return render(request, 'all_customer/book.html', )


def payment(request):
      return render(request, 'all_customer/payment.html', )
