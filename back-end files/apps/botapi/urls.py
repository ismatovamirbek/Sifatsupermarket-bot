from django.urls import path
from .views import ChanelAPIView

urlpatterns = [
    path("channels/", ChanelAPIView.as_view()),
]