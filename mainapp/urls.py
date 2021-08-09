from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
  path('', views.index, name='home'),
  path('about/', views.about, name='about'),
  path('contact/', views.contact, name='contact'),
  path('accounts/register/', views.signup, name='register'),
  path('accounts/login/', views.sign_in, name='login'),
  path('accounts/logout/', views.logout_user, name='logout'),
  path('api/bookings/', views.BookingList.as_view()),
  path('api-token-auth/', views.obtain_auth_token),
  path('api/booking/<booking_id>', views.BookingItem.as_view()),
  path('api/allunits/', views.AllUnits.as_view(),),
  path('api/aUnit/<int:id>', views.OneUnit.as_view(),),
  path('mainadmin/', views.customadmin, name='customadmin'),
  path('mainadminpost/', views.mainadminpost, name='mainadminpost')
]
if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
  urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
