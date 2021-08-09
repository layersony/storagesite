from django.shortcuts import render ,redirect,get_object_or_404
from django.http import HttpResponseRedirect
from . forms import BookingForm,AddUserForm
from .models import User ,Profile,Booking,Unit
from mainapp import views

def units(request):
    units = Unit.objects.all()

    return render (request,'employee/units.html' ,{'units':units})


def onsite_booking(request):
    users = User.objects.exclude(id=request.user.id)

    if request.method == 'POST':
        form = BookingForm(request.POST, request.FILES)
        user_form = AddUserForm(request.POST)

        if form.is_valid():
            book_unit = form.save(commit=False)
            book_unit.save()
            return redirect('onsite_booking')

        if user_form.is_valid():
            add_user = user_form.save(commit=False)
            add_user.set_password(user_form.cleaned_data['password1'])
            add_user.save()
            return  redirect('onsite_booking') 
    else:
        form = BookingForm()
        views.customadmin
        user_form = AddUserForm()
    return render(request, 'employee/onsite_booking.html', { 'user_form': user_form, 'form': form,'users': users})


def search(request):
    current_user = request.user
    all_units = Unit.objects.all()
    parameter = request.GET.get('unit')
    searched_units = Unit.objects.filter(name__icontains=parameter)

    return render(request,'search_result.html',{'current_user':current_user,'units':searched_units})


def delete_unit(request,unit_id):
    current_user = request.user
    unit = Unit.objects.get(pk=unit_id)
    if unit:
        unit.delete_unit(unit_id)
    return redirect('units')


