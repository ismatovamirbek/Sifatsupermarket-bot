from rest_framework import generics, status
from .models import BotUser, VacancyApplication
from .serializers import BotUserSerializer, VacancyApplicationSerializer
from rest_framework.response import Response


class BotUserCreateView(generics.CreateAPIView):
    queryset = BotUser.objects.all()
    serializer_class = BotUserSerializer

class BotUserListView(generics.ListAPIView):
    queryset = BotUser.objects.all()
    serializer_class = BotUserSerializer

class BotUserUpdateView(generics.RetrieveUpdateAPIView):
    queryset = BotUser.objects.all()
    serializer_class = BotUserSerializer
    lookup_field = 'telegram_id'

# 🔄 ViewSet o‘rniga CreateAPIView ishlatamiz
class VacancyApplicationCreateView(generics.CreateAPIView):
    queryset = VacancyApplication.objects.all()
    serializer_class = VacancyApplicationSerializer

    def create(self, request, *args, **kwargs):
        telegram_id = request.data.get("telegram_id")
        if VacancyApplication.objects.filter(telegram_id=telegram_id).exists():
            return Response(
                {"detail": "Siz allaqachon ariza topshirgansiz."},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().create(request, *args, **kwargs)
