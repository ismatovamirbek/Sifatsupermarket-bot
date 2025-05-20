from rest_framework import status

from .serializers import ChanelSerializer
from .models import Chanel
from rest_framework.views import APIView
from rest_framework.response import Response


class ChanelAPIView(APIView):
    def get(self, request):
        channels = Chanel.objects.all()
        serializer = ChanelSerializer(channels, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ChanelSerializer(data=request.data)
        if serializer.is_valid():
            chanel_id = serializer.validated_data.get("chanel_id")
            if Chanel.objects.filter(chanel_id=chanel_id).exists():
                return Response({"detail": "Bu kanal allaqachon mavjud."}, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
