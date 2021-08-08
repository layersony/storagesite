from django.urls import path
from . import views 

urlpatterns = [
  path('employee/', views.employee, name='employee'),
  path('units', views.units, name='units'),
  path('onsite_booking/', views.onsite_booking, name='onsite_booking'),
  
]