from django.http.response import JsonResponse
from django.shortcuts import render ,redirect,get_object_or_404
from django.http import HttpResponseRedirect
from . forms import BookingForm,AddUserForm
from .models import User ,Profile,Booking,Unit
from mainapp import views
from django.contrib import messages

def employee(request):
    pickup=Booking.objects.filter(pickup=True)
    delivery=Booking.objects.filter(delivery=True)
    available=Unit.objects.filter(occupied=False)
    occupied_units=Unit.objects.filter(occupied=True)
    users=User.objects.filter(user_type='client')
    return render(request,'employee.html' ,{'pickup' :pickup,'delivery' :delivery, 'available' :available, 'occupied_units' :occupied_units, 'users' :users}) 

def units(request):
    units = Unit.objects.all()
    return render (request,'employee/units.html' ,{'units':units})


def onsite_booking(request, unit_name):
    users = User.objects.exclude(id=request.user.id)
    unit = Unit.objects.get(name=unit_name)

    if request.method == 'POST':
        form = BookingForm(request.POST, request.FILES)
        user_form = AddUserForm(request.POST)

        user_full_name = request.POST.get('user_profile')

        user_obj = User.objects.get(name=user_full_name)

        profile_obj = Profile.objects.get(user=user_obj)

        if form.is_valid():
            book_unit = form.save(commit=False)
            book_unit.proofile = profile_obj
            book_unit.unit = unit
            book_unit.save()
            messages.success(request, 'Booked Successfully.')
            return redirect('')

        if user_form.is_valid():
            add_user = user_form.save(commit=False)
            add_user.set_password(user_form.cleaned_data['password1'])
            add_user.save()
            messages.success(request, 'Booked successfully.')
            return  redirect('onsite_booking') 
    else:
        form = BookingForm()
        views.customadmin
        user_form = AddUserForm()
        messages.success(request, 'Booked successfully.')
    return render(request, 'employee/onsite_booking.html', { 'user_form': user_form, 'form': form,'users': users, 'unit':unit})


def search(request):
    current_user = request.user
    if request.method == "POST":
        parameter = request.POST.get('search')
        searched_unit = Unit.objects.filter(name__icontains=parameter)
        
        return render(request,'employee/search_result.html',{'current_user':current_user,'units':searched_unit})

    return render(request,'employee/search_result.html',{'current_user':current_user,'units':[]})


def delete_unit(request,unit_name):
    current_user = request.user
    unit = Unit.objects.get(name=unit_name)
    if unit:
        Unit.delete_unit(unit_name)
        messages.success(request, 'Deleted successfully')
    return redirect('units')

def search_client(request):
    client = request.GET.get('client')

    payload = []
    if client:
        clients = User.objects.filter(user_type='client',name__icontains=client)
        for client in clients:
            payload.append(client.name)

    return JsonResponse({'status': 200, 'data': payload})



