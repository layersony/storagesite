from django.urls import path
from . import views

urlpatterns = [
  path('available', views.available, name='available'),
  path('book/', views.book, name='book'),
  path('payment/', views.payment, name='payment'),
]

