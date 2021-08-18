from django.http.response import JsonResponse
from django.shortcuts import render ,redirect,get_object_or_404
from django.http import HttpResponseRedirect
from . forms import BookingForm,AddUserForm
from .models import User ,Profile,Booking,Unit
from mainapp import views
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def employee(request):
    user_type = request.user.user_type
    if user_type != 'employee':
        messages.error(request, 'Please log in as an employee to access this view.')
        return redirect('login')

    pickup=Booking.objects.filter(pickup=True)
    delivery=Booking.objects.filter(delivery=True)
    available=Unit.objects.filter(occupied=False)
    occupied_units=Unit.objects.filter(occupied=True)
    users=User.objects.filter(user_type='client')
    return render(request,'employee.html' ,{'pickup' :pickup,'delivery' :delivery, 'available' :available, 'occupied_units' :occupied_units, 'users' :users}) 

@login_required(login_url='login')
def units(request):
    user_type = request.user.user_type
    if user_type != 'employee':
        messages.error(request, 'Please log in as an employee to access this view.')
        return redirect('login')
    units = Unit.objects.all()
    return render (request,'employee/units.html' ,{'units':units})

@login_required(login_url='login')
def onsite_booking(request, unit_name):
    user_type = request.user.user_type
    if user_type != 'employee':
        messages.error(request, 'Please log in as an employee to access this view.')
        return redirect('login')

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

            # payment process
            payment = form.cleaned_data['payment_mode']
            accountnumber = form.cleaned_data['account_number']
            Booking.lipa_booking(request, unit.id, accountnumber, payment)

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

@login_required(login_url='login')
def search(request):
    user_type = request.user.user_type
    if user_type != 'employee':
        messages.error(request, 'Please log in as an employee to access this view.')
        return redirect('login')

    current_user = request.user
    if request.method == "POST":
        parameter = request.POST.get('search')
        searched_unit = Unit.objects.filter(name__icontains=parameter)
        
        return render(request,'employee/search_result.html',{'current_user':current_user,'units':searched_unit})

    return render(request,'employee/search_result.html',{'current_user':current_user,'units':[]})

@login_required(login_url='login')
def delete_unit(request,unit_name):
    user_type = request.user.user_type
    if user_type != 'employee':
        messages.error(request, 'Please log in as an employee to access this view.')
        return redirect('login')

    unit = Unit.objects.get(name=unit_name)
    if unit:
        Unit.delete_unit(unit_name)
        messages.success(request, 'Deleted successfully')
    return redirect('units')

@login_required(login_url='login')
def search_client(request):
    user_type = request.user.user_type
    if user_type != 'employee':
        messages.error(request, 'Please log in as an employee to access this view.')
        return redirect('login')

    client = request.GET.get('client')

    payload = []
    if client:
        clients = User.objects.filter(user_type='client',name__icontains=client)
        for client in clients:
            payload.append(client.name)

    return JsonResponse({'status': 200, 'data': payload})



