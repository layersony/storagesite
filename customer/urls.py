from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
  # path('', views.index, name='custhome'),
  path('profile/', views.Profile, name='profile'),
  path('bookingdatail/', views.bookingDetails, name = 'boolingdetials'),
  path('profile/update', views.ProfileUpdate, name='update_profile'),
  path('available/', views.available, name='available'),
  path('book/', views.book, name='book'),
  path('payment/', views.payment, name='payment'),
]

