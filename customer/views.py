from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import logout, login, authenticate
from .models import user_type, User
from .forms import RegistrationForm
from django.contrib import messages

from .forms import UpdateProfileForm
from django.contrib.auth.models import User
from mainapp.models import Profile
from . import views
from django.conf import settings

User = settings.AUTH_USER_MODEL

def index(request):
  return HttpResponse('Am Customer')

def updateProfile(request, username):
    user = User.objects.get(username=username)
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('profile', user.username)
    else:
        form = UpdateProfileForm()
    return render(request, 'updateProfile.html', {'form': form})


def profile(request, username):
    return render(request, 'profile.html')

