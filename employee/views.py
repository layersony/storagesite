from django.shortcuts import render ,redirect,get_object_or_404
from django.http import HttpResponseRedirect
from . forms import BookingForm,AddUserForm
from .models import User ,Profile,Booking,Unit
from mainapp import views

def units(request):
    return render (request,'employee/units.html')


def onsite_booking(request):
    users = User.objects.exclude(id=request.user.id)
    if request.method == 'POST':
        form = BookingForm(request.POST, request.FILES)
        user_form = AddUserForm(request.POST)

        if form.is_valid():
            upload = form.save(commit=False)
            upload.user = request.user.profile
            upload.save()
            return HttpResponseRedirect(request.path_info)

        if user_form.is_valid():
            add_user = user_form.save(commit=False)
            add_user.set_password(user_form.cleaned_data['password1'])
            add_user.save()
            return  redirect('onsite_booking') 
    else:
        form = BookingForm()
        views.customadmin
        user_form = AddUserForm()
    return render(request, 'employee/onsite_booking.html', { 'user_form': user_form, 'form': form,'users': users,})

