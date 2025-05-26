from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from rest_framework import status
from monitorizacao.models import SegmentoEstrada as Segmento, Leitura

class SegmentoAPITestCase(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(username='admin', password='adminpass')
        self.anon_client = APIClient()

        self.admin_client = APIClient()
        self.admin_client.login(username='admin', password='adminpass')

        self.segmento = Segmento.objects.create(nome="Rua X")

    def test_admin_can_create_segmento(self):
        data = {"nome": "Rua Nova"}
        response = self.admin_client.post('/api/segmentos/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_anon_cannot_create_segmento(self):
        data = {"nome": "Rua Bloqueada"}
        response = self.anon_client.post('/api/segmentos/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_anon_can_read_segmentos(self):
        response = self.anon_client.get('/api/segmentos/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
