from django.shortcuts import render ,redirect,get_object_or_404
from django.http import HttpResponseRedirect
from . forms import BookingForm
from .models import User ,Profile,Booking,Unit


def units(request):
    return render (request,'employee/units.html')


def onsite_booking(request):
    users = User.objects.exclude(id=request.user.id)
    if request.method == 'POST':
        form = BookingForm(request.POST, request.FILES)
        if form.is_valid():
            upload = form.save(commit=False)
            upload.user = request.user.profile
            upload.save()
            return HttpResponseRedirect(request.path_info)
    else:
        form = BookingForm()
    return render(request, 'employee/onsite_booking.html', {'form': form,'users': users,})
