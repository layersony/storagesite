from django.shortcuts import render ,redirect,get_object_or_404
from django.http import HttpResponseRedirect
from .forms import BookingForm,PaymentForm


from .models import User ,Profile,Booking,Unit

def available(request):
      units=Unit.objects.all()
      return render(request, 'all_customer/available_units.html', {"units":units})



def book(request, pk=None):
      if pk:
            unit=Unit.objects.get(pk=pk)
      else:
            unit = request.user
      
      form_class = BookingForm()
      form = BookingForm()

      if request.method == 'POST':
            form = BookingForm(request.POST)
            if form.is_valid():
                  form.save()

      context = {'form': form}
      return render(request, 'all_customer/book.html',  context)


def payment(request):
      form_class = PaymentForm()
      form = PaymentForm()

      if request.method == 'POST':
            form = PaymentForm(request.POST)
            if form.is_valid():
                  form.save()

      context = {'form': form}
      return render(request, 'all_customer/payment.html', context)




      
      
