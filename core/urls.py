"""
Configuração de URLs para o projeto principal (core).

Este arquivo mapeia as URLs para as views da aplicação.
Para mais informações: https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""

from django.conf import settings
from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path
from django.views.generic.base import RedirectView
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from orders.views import OrderViewSet
from products.views import ProductViewSet

# --- 1. View para a Raiz da API ---


def api_root(request):
    return JsonResponse(
        {
            "status": "ok",
            "message": "Bem-vindo(a) à API do projeto Backend-template!",
            "version": "v1",
            "links": {
                "products": "/api/v1/products/",
                "orders": "/api/v1/orders/",
            },
        }
    )


# --- 2. Configuração do Roteador do DRF ---
router = DefaultRouter()
router.register(r"products", ProductViewSet, basename="product")
router.register(r"orders", OrderViewSet, basename="order")

# --- 3. Lista Principal de Padrões de URL ---
urlpatterns = [
    path("", RedirectView.as_view(url="/api/v1/", permanent=False), name="index"),
    path("admin/", admin.site.urls),
    path("api-token-auth/", obtain_auth_token, name="api_token_auth"),
    path("api/v1/", api_root, name="api-root"),
    path("api/v1/", include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]
