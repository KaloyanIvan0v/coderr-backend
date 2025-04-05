
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('user_auth_app.api.urls')),
    path('api/', include('core_app.api.urls')),
]
