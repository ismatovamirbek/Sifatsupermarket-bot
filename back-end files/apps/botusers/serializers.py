from rest_framework import serializers
from .models import BotUser, VacancyApplication

class BotUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BotUser
        fields = '__all__'  # yoki fields = ['telegram_id', 'first_name', 'last_name', 'username', 'created_at', 'is_active']


class VacancyApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = VacancyApplication
        fields = '__all__'