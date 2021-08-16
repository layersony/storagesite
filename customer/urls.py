from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
  # path('', views.index, name='custhome'),
  path('profile/', views.profile, name='profile'),
  path('profile/bookingdetail/<str:id>', views.booking_details, name = 'bookingdetails'),
  path('profile/update/', views.update_profile, name='update_profile'),
  path('available/', views.available, name='available'),
  path('book/<str:pk>', views.book, name='book'),
  # path('payment/', views.payment, name='payment'),
  path('ajax/checkout', views.checkout, name='checkout')
]


