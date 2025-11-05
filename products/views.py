# from rest_framework.authentication import (
#     BasicAuthentication,
#     SessionAuthentication,
#     TokenAuthentication,
# )
# from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .models import Product
from .serializers import ProductSerializer


class ProductViewSet(ModelViewSet):
    # authentication_classes = [
    #     TokenAuthentication,
    #     SessionAuthentication,
    #     BasicAuthentication,
    # ]
    # permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializer

    queryset = Product.objects.all().order_by("id")
