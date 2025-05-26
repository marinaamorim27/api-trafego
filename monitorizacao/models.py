import uuid
from django.db import models
from django.utils import timezone

class SegmentoEstrada(models.Model):
    nome = models.CharField(max_length=100)


    def __str__(self):
        return self.nome
    
class Leitura(models.Model):
    segmento = models.ForeignKey(SegmentoEstrada, on_delete=models.CASCADE, related_name='leituras')
    data_hora = models.DateTimeField()
    velocidade_media = models.FloatField()

    def __get_intensidade__(self):
        if self.velocidade_media <= 20:
            return "elevada"
        elif self.velocidade_media <= 50:
            return "média"
        else:
            return "baixa"
        
        
class Sensor(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.uuid})"

class Carro(models.Model):
    license_plate = models.CharField(max_length=10, unique=True)
    registado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.license_plate

class RegistoPassagem(models.Model):
    carro = models.ForeignKey(Carro, on_delete=models.CASCADE)
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    segmento = models.ForeignKey("SegmentoEstrada", on_delete=models.CASCADE)
    timestamp = models.DateTimeField()

    def __str__(self):
        return f"{self.carro} - {self.timestamp}"