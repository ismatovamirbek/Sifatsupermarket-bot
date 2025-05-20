from django.urls import path
from .views import (
    BotUserCreateView, BotUserListView, BotUserUpdateView,
    VacancyApplicationCreateView
)

urlpatterns = [
    path('create/', BotUserCreateView.as_view(), name='bot-user-create'),
    path('list/', BotUserListView.as_view(), name='bot-user-list'),
    path('update/<int:telegram_id>/', BotUserUpdateView.as_view(), name='bot-user-update'),
    path('vacancy-applications/', VacancyApplicationCreateView.as_view(), name='vacancy-create'),
]
