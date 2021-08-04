from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import logout, login, authenticate
from .models import user_type, User
from .forms import RegistrationForm
from django.contrib import messages

def index(request):
  return HttpResponse('Am MainApp '+ str(request.user))

def signup(request):
  if request.method == 'POST':
    form = RegistrationForm(request.POST)
    if form.is_valid():
      temail = request.POST.get('email')
      password = request.POST.get('password1')
      user = form.cleaned_data.get('username')
      usertype = 'customer'
      messages.success(request, 'Account was created for ' + user)
      form.save()
      user = User.objects.get(email=temail)

      usert = None

      if usertype == 'customer':
        usert = user_type(user=user,is_customer=True)
      usert.save()

      user = authenticate(request, email=temail, password=password)

      if user is not None:
          login(request, user)
          type_obj = user_type.objects.get(user=user)
          if user.is_authenticated and type_obj.is_employee:
              return redirect('emphome') 
          elif user.is_authenticated and type_obj.is_customer:
              return redirect('custhome')

      return redirect('home')

    else:
      messages.info(request, 'Error Processing Your Request')
      params = {
        'form': form
      }
      return render(request, 'registration/register.html', params)

  form = RegistrationForm()
  params = {
    'form' : form
  }
  return render(request, 'registration/register.html', params)

def sign_in(request):
    if request.method == 'POST':
        email = request.POST.get('email') 
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            type_obj = user_type.objects.get(user=user)
            if user.is_authenticated and type_obj.is_employee:
                return redirect('emphome') 
            elif user.is_authenticated and type_obj.is_customer:
                return redirect('custhome')
        else:
          messages.info(request, 'Username Or Password is incorrect')
          return redirect('login')
    return render(request, 'registration/login.html')

def logout_user(request):
  logout(request)
  return redirect('home')