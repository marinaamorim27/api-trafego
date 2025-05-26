from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets, permissions
from .models import SegmentoEstrada, Leitura, Carro, Sensor, RegistoPassagem
from .serializers import SegmentoEstradaSerializer, LeituraSerializer
from django.utils import timezone
from datetime import timedelta
from rest_framework.decorators import api_view
from .serializers import RegistoPassagemSerializer

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.is_staff:
            return True
        return request.method in permissions.SAFE_METHODS

class SegmentoEstradaViewSet(viewsets.ModelViewSet):
    queryset = SegmentoEstrada.objects.all()
    serializer_class = SegmentoEstradaSerializer
    permission_classes = [IsAdminOrReadOnly]

class LeituraViewSet(viewsets.ModelViewSet):
    queryset = Leitura.objects.all()
    serializer_class = LeituraSerializer
    permission_classes = [IsAdminOrReadOnly]


class RegistoPassagemBulkCreateView(APIView):
    API_KEY = "23231c7a-80a7-4810-93b3-98a18ecfbc42"

    def post(self, request):
        api_key = request.headers.get("X-API-KEY")
        if api_key != self.API_KEY:
            return Response({"detail": "API Key inválida"}, status=status.HTTP_403_FORBIDDEN)

        data = request.data
        for item in data:
            license_plate = item["car__license_plate"]
            carro, _ = Carro.objects.get_or_create(license_plate=license_plate)

            sensor_uuid = item["sensor__uuid"]
            try:
                sensor = Sensor.objects.get(uuid=sensor_uuid)
            except Sensor.DoesNotExist:
                return Response({"detail": f"Sensor {sensor_uuid} não encontrado"}, status=status.HTTP_400_BAD_REQUEST)

            segmento = SegmentoEstrada.objects.get(id=item["road_segment"])
            timestamp = item["timestamp"]

            RegistoPassagem.objects.create(
                carro=carro,
                sensor=sensor,
                segmento=segmento,
                timestamp=timestamp
            )

        return Response({"detail": "Registos criados com sucesso"}, status=status.HTTP_201_CREATED)
    
@api_view(["GET"])
def passagens_ultimas_24h(request):
    matricula = request.query_params.get("matricula")
    if not matricula:
        return Response({"detail": "Parâmetro 'matricula' é obrigatório"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        carro = Carro.objects.get(license_plate=matricula)
    except Carro.DoesNotExist:
        return Response({"detail": "Carro não encontrado"}, status=status.HTTP_404_NOT_FOUND)

    ontem = timezone.now() - timedelta(hours=24)
    passagens = RegistoPassagem.objects.filter(carro=carro, timestamp__gte=ontem)

    serializer = RegistoPassagemSerializer(passagens, many=True)
    return Response(serializer.data)