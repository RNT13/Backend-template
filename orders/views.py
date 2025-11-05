from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .models import Order
from .serializers import OrderCreateSerializer, OrderReadSerializer


class OrderViewSet(ModelViewSet):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all().prefetch_related("items", "items__product")

    def get_serializer_class(self):
        if self.action == "create":
            return OrderCreateSerializer

        return OrderReadSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        if not self.request.user.is_superuser:
            return queryset.filter(user=self.request.user)

        return queryset.order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
