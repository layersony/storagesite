from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
  # path('', views.index, name='custhome'),
  path('profile/', views.profile, name='profile'),
  path('bookingdatail', views.views.bookingDetails, name = 'boolingdetials'),
  path('update/', views.updateProfile, name='updateProfile'),
  path('available/', views.available, name='available'),
  path('book/', views.book, name='book'),
  path('payment/', views.payment, name='payment'),
]

