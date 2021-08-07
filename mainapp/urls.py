from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
  path('', views.index, name='home'),
  path('accounts/register/', views.signup, name='register'),
  path('accounts/login/', views.sign_in, name='login'),
  path('accounts/logout/', views.logout_user, name='logout'),
  path('api/bookings/', views.BookingList.as_view()),
  path('api-token-auth/', views.obtain_auth_token),
  path('api/booking/<booking_id>', views.BookingItem.as_view()),
  path('api/allunits/', views.AllUnits.as_view(),),
  path('api/aUnit/<int:id>', views.OneUnit.as_view(),),
  path('mainadmin/', views.customadmin, name='customadmin'),
  path('mainadmin/user/<str:id>/', views.mainadminupdateuser, name='mainadminupdateuser'),
  path('mainadmin/user/delete/<str:id>', views.deleteuser, name='deleteuser'),

  path('mainadmin/userprofile/<str:id>/', views.mainadminupdateprofile, name='mainadminupdateprofile'),
  path('mainadmin/userprofile/delete/<str:id>', views.deleteprofile, name='deleteprofile'),

  path('mainadmin/userunit/<str:id>/', views.mainadminupdateunit, name='mainadminupdateunit'),
  path('mainadmin/userunit/delete/<str:id>', views.deleteunit, name='deleteunit'),

  path('mainadmin/userbook/<str:id>/', views.mainadminupdatebook, name='mainadminupdatebook'),
  path('mainadmin/userbook/delete/<str:id>', views.deletebook, name='deletebook'),
]
if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
  urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
