from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, authenticate
from .forms import RegistrationForm
from django.contrib import messages

def index(request):
  return render(request, 'index.html')

def signup(request):

  if request.method == 'POST':
    form = RegistrationForm(request.POST)
    if form.is_valid():
      temail = request.POST.get('email')
      password = request.POST.get('password1')
      clientname = form.cleaned_data.get('username')
      messages.success(request, 'Account was created for ' + clientname)

      regform = form.save(commit=False)
      regform.user_type='client'
      regform.save()

      user = authenticate(request, email=temail, password=password)

      if user is not None:
          login(request, user) 
          if user.is_authenticated and (user.user_type=='client'):
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
          if user.is_authenticated and user.is_superuser:
            return redirect('admin:index')
          elif user.is_authenticated and (user.user_type=='employee'):
            return redirect('emphome') 
          elif user.is_authenticated and (user.user_type=='client'):
            return redirect('custhome')
      else:
        messages.info(request, 'Username Or Password is incorrect')
        return redirect('login')
  return render(request, 'registration/login.html')

def logout_user(request):
  logout(request)
  return redirect('home')
