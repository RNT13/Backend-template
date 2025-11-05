from django.db import transaction
from rest_framework import serializers

from products.models import Product
from products.serializers import ProductSerializer

from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):

    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ["id", "product", "quantity", "price"]


# --- Serializer para Ler/Listar Pedidos ---


class OrderReadSerializer(serializers.ModelSerializer):

    items = OrderItemSerializer(many=True, read_only=True)
    user = serializers.StringRelatedField()

    class Meta:
        model = Order
        fields = ["id", "user", "created_at", "total_price", "items"]


# --- Serializer para a Criação de Pedidos ---


class OrderItemCreateSerializer(serializers.Serializer):

    product_id = serializers.UUIDField()
    quantity = serializers.IntegerField(min_value=1)

    def validate_product_id(self, value):
        try:
            product = Product.objects.get(id=value)
            if not product:
                raise serializers.ValidationError("Produto não encontrado.")
        except Product.DoesNotExist:
            raise serializers.ValidationError("Produto não encontrado.")
        return value


class OrderCreateSerializer(serializers.ModelSerializer):

    items = OrderItemCreateSerializer(many=True, write_only=True)

    class Meta:
        model = Order
        fields = ["id", "items", "user", "total_price"]
        read_only_fields = ["user", "total_price"]

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        user = validated_data.pop("user")

        with transaction.atomic():
            total_price = 0
            products_to_update = []

            for item_data in items_data:
                try:
                    product = Product.objects.get(id=item_data["product_id"])
                except Product.DoesNotExist:
                    raise serializers.ValidationError(f"Produto com ID {item_data['product_id']} não encontrado.")

                if product.stock < item_data["quantity"]:
                    raise serializers.ValidationError(
                        f"Estoque insuficiente para o produto '{product.name}'. Disponível: {product.stock}."
                    )

                total_price += product.price * item_data["quantity"]

                product.stock -= item_data["quantity"]
                products_to_update.append(product)

            order = Order.objects.create(user=user, total_price=total_price)

            order_items_to_create = []
            for item_data in items_data:
                product = Product.objects.get(id=item_data["product_id"])
                order_items_to_create.append(
                    OrderItem(
                        order=order,
                        product=product,
                        quantity=item_data["quantity"],
                        price=product.price,
                    )
                )

            OrderItem.objects.bulk_create(order_items_to_create)

            Product.objects.bulk_update(products_to_update, ["stock"])

            return order
