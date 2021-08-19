from django.contrib import admin
from django.urls import path
from django.conf.urls import include

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', include('mainapp.urls')),
    path('customer/', include('customer.urls')),
    path('employee/', include('employee.urls')),
    path('api/v1/', include('mpesa_api.urls')),
]