from django.urls import path, include

urlpatterns = [
    path('botusers/', include('botusers.urls')),
    path('botapi/', include('botapi.urls')),
]