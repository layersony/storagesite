from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
  path('', views.index, name='home'),
  path('accounts/register/', views.signup, name='register'),
  path('accounts/login/', views.sign_in, name='login'),
  path('accounts/logout/', views.logout_user, name='logout'),
  path('api/bookings', views.BookingList.as_view())
]
if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
  urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
