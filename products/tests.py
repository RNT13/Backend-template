from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient

from products.factory import ProductFactory


class ProductAPITestCase(TestCase):
    def setUp(self):
        """Este método roda antes de cada teste."""
        # 1. Cria um usuário de teste
        self.user = User.objects.create_user(username="testuser", password="testpassword")

        # 2. Cria um cliente de API
        self.client = APIClient()

        # 3. Força a autenticação do cliente com o usuário criado
        self.client.force_authenticate(user=self.user)

    def test_list_products(self):
        """Testa se a listagem de produtos funciona para um usuário autenticado."""
        # Cria 3 produtos no banco de dados de teste
        ProductFactory.create_batch(3)

        # Faz a requisição GET para a API (agora autenticada)
        response = self.client.get("/api/v1/products/")

        # Verifica se a resposta foi bem-sucedida (status 200)
        self.assertEqual(response.status_code, 200)

        # Verifica se a resposta contém 3 produtos
        self.assertEqual(response.data["count"], 3)
