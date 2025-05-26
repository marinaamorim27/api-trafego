from rest_framework import viewsets, permissions
from .models import SegmentoEstrada, Leitura
from .serializers import SegmentoEstradaSerializer, LeituraSerializer

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
