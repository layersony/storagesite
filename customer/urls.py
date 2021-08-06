from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
  path('', views.index, name='custhome'),
  path('', views.index, name='index'),
  path('account/', include('django.contrib.auth.urls')),
  path('profile/<username>', views.profile, name='profile'),
  path('profile/<username>/edit/', views.updateProfile, name='updateProfile'),
]