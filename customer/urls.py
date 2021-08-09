from django.urls import path
from . import views

urlpatterns = [
  path('available', views.available, name='available'),
  path('book/', views.book, name='book'),
  path('book/(?P<pk>\d+)/$', views.book, name='book_with_pk'),
  path('payment/', views.payment, name='payment'),
]


