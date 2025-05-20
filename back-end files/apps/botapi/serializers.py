from rest_framework import serializers
from .models import Chanel

class ChanelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chanel
        fields = ("chanel_name", "chanel_id", "chanel_username", "created_at", "updated_at")
        read_only_fields = ("created_at", "updated_at")