from django.urls import path
from . import views 

urlpatterns = [
  path('employee/', views.employee, name='employee'),
  path('units', views.units, name='units'),
  path('onsite_booking/', views.onsite_booking, name='onsite_booking'),
  path('search_result',views.search, name="search" ),
  path('delete_unit/<unit_id>',views.delete_unit,name='delete_unit'),

]