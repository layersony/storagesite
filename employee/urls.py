from django.urls import path
from . import views

urlpatterns = [
  path('', views.index, name='home'),
  path('units', views.units, name='units'),
  
]