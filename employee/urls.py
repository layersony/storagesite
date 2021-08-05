from django.urls import path
from . import views

urlpatterns = [
  path('', views.index, name='emphome'),
  path('units', views.units, name='units'),
  
]