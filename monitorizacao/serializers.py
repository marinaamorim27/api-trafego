from rest_framework import serializers
from .models import SegmentoEstrada, Leitura

class LeituraSerializer(serializers.ModelSerializer):
    intensidade = serializers.SerializerMethodField()

    class Meta:
        model = Leitura
        fields = ['id', 'segmento', 'velocidade_media', 'data_hora', 'intensidade']

    def get_intensidade(self, obj):
        return obj.get_intensidade()

class SegmentoEstradaSerializer(serializers.ModelSerializer):
    total_leituras = serializers.SerializerMethodField()

    class Meta:
        model = SegmentoEstrada
        fields = ['id', 'nome', 'total_leituras']

    def get_total_leituras(self, obj):
        return obj.leituras.count()
