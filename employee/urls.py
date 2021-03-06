from django.urls import path
from . import views 

urlpatterns = [
  path('', views.employee, name='employee'),
  path('units', views.units, name='units'),
  path('onsite_booking/<unit_name>', views.onsite_booking, name='onsite_booking'),
  path('search/',views.search, name='search' ),
  path('delete_unit/<unit_name>',views.delete_unit,name='delete_unit'),
  path('search_client/',views.search_client, name='search_client' ),

]