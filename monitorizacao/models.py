from django.db import models

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