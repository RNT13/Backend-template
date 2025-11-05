import pytest
from rest_framework.test import APIClient

from .factories import ProductFactory


@pytest.mark.django_db
def test_list_products():
    ProductFactory.create_batch(3)
    client = APIClient()
    response = client.get("/api/products/")
    assert response.status_code == 200
    assert len(response.data["results"]) == 3
