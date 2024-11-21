from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('',  HomeView.as_view(),),
    path('admin/', admin.site.urls),  # Admin interface
    path('api/v1/', include('events.urls')),  # Include app-level URL patterns
]
