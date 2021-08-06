from django.urls import path
from . import views

urlpatterns = [
  path('', views.available, name='available'),
  path('book/', views.book, name='book'),
  path('payment/', views.payment, name='payment'),
]

