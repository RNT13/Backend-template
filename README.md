# Backend API de Vendas 🐍

Um template robusto de backend construído com **Django** e **Django REST Framework**, projetado para gerenciar produtos e pedidos. O projeto utiliza **Poetry** para gerenciamento de dependências, **PostgreSQL** como banco de dados, e é totalmente containerizado com **Docker**.

Inclui autenticação por token, testes automatizados com **pytest**, e um fluxo de trabalho de CI/CD com **GitHub Actions**, garantindo um desenvolvimento rápido, padronizado e profissional para qualquer solução de e-commerce ou API REST. 🚀

---

## 📖 Índice

1. [**Como Usar o Projeto (Guia Rápido)**](#-1-como-usar-o-projeto-guia-rápido)

   - [Clonar o Projeto](#-11-clonar-o-projeto)
   - [Configurar o `.env`](#-12-configurar-o-arquivo-env)
   - [Subir os Containers com Docker](#-13-subir-os-containers-com-docker)
   - [Aplicar Migrações e Criar Superusuário](#-14-aplicar-migrações-e-criar-superusuário)
   - [Endpoints da API](#-15-endpoints-da-api)
   - [Rodar Testes e Ferramentas de Qualidade](#-16-rodar-testes-e-ferramentas-de-qualidade)

2. [**Como Construir Este Projeto do Zero (Tutorial)**](#-2-como-construir-este-projeto-do-zero-tutorial)

   - [Etapa 1: Criar o Projeto Base](#etapa-1--criar-o-projeto-base-com-poetry-e-django)
   - [Etapa 2: Estrutura de Diretórios](#etapa-2--estrutura-de-diretórios)
   - [Etapa 3: Configuração do Django](#etapa-3--configuração-do-django)
   - [Etapa 4: Models](#etapa-4--models-básicos)
   - [Etapa 5: Serializers e Views](#etapa-5--serializers-e-views)
   - [Etapa 6: URLs](#etapa-6--urls)
   - [Etapa 7: Testes com Pytest](#etapa-7--testes-com-pytest--factory_boy--faker)
   - [Etapa 8: Makefile](#etapa-8--makefile-básico)
   - [Etapa 9: Docker e Docker Compose](#etapa-9--docker--docker-compose)
   - [Etapa 10: GitHub Actions (CI)](#etapa-10--github-actions)

---

## 🚀 1. Como Usar o Projeto (Guia Rápido)

Esta seção é para quem deseja rodar o projeto rapidamente.

### ✅ 1.1. Clonar o Projeto

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

### ✅ 1.2. Configurar o Arquivo .env

Crie um arquivo .env na raiz do projeto. Ele guardará as variáveis de ambiente para a aplicação e o banco de dados.

```env
# Configurações do Django
DEBUG=1
SECRET_KEY=sua-chave-secreta-super-forte-aqui
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1

# Configurações do Banco de Dados (PostgreSQL )
SQL_ENGINE=django.db.backends.postgresql
SQL_DATABASE=BackendTemplate_dev_db
SQL_USER=BackendTemplate_dev
SQL_PASSWORD=BackendTemplate123
SQL_HOST=db
SQL_PORT=5432
```

Atenção: Os valores do banco de dados devem ser os mesmos definidos no seu docker-compose.yml.

### ✅ 1.3. Subir os Containers com Docker

Com o Docker e o Docker Compose instalados, suba os serviços web (Django) e db (PostgreSQL).

```bash
docker-compose up -d --build
```

O serviço web estará acessível em [http://localhost:8000](http://localhost:8000).
Para visualizar os logs: `docker-compose logs -f web`.

### ✅ 1.4. Aplicar Migrações e Criar Superusuário

```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

Acesse o painel de administração em: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/).

### ✅ 1.5. Endpoints da API

Para interagir com a API, primeiro obtenha um token de autenticação.

**Endpoint de Autenticação:** `POST /api-token-auth/`

```json
{
  "username": "seu-usuario",
  "password": "sua-senha"
}
```

Use o token recebido no cabeçalho `Authorization: Token seu_token_aqui`.

**Endpoints Principais (/api/v1/)**

| Método         | Endpoint               | Descrição                                    |
| -------------- | ---------------------- | -------------------------------------------- |
| GET/POST       | /api/v1/products/      | Lista ou cria produtos.                      |
| GET/PUT/DELETE | /api/v1/products/{id}/ | Detalha, atualiza ou deleta um produto.      |
| GET/POST       | /api/v1/orders/        | Lista os pedidos do usuário ou cria um novo. |
| GET            | /api/v1/orders/{id}/   | Detalha um pedido específico.                |

### ✅ 1.6. Rodar Testes e Ferramentas de Qualidade

```bash
# Rodar testes
docker-compose exec web poetry run pytest -v

# Rodar linters e formatadores
docker-compose exec web poetry run black .
docker-compose exec web poetry run isort .
docker-compose exec web poetry run flake8 .
```

## 🛠️ 2. Como Construir Este Projeto do Zero (Tutorial)

### ETAPA 1 — Criar o Projeto Base com Poetry e Django

```bash
mkdir BackendTemplate
cd BackendTemplate

# Inicializa o projeto e adiciona as dependências
poetry init -n
poetry add django djangorestframework psycopg2-binary django-extensions
poetry add black isort flake8 pytest pytest-django factory-boy faker --group dev

# Crie o projeto Django:
poetry run django-admin startproject core .
```

### ETAPA 2 — Estrutura de Diretórios

```bash
poetry run python manage.py startapp products
poetry run python manage.py startapp orders
```

Estrutura final:

```
/
├── core/
├── products/
├── orders/
├── .github/workflows/
├── .env
├── manage.py
├── pyproject.toml
├── Dockerfile
└── docker-compose.yml
```

### ETAPA 3 — Configuração do Django

No arquivo `core/settings.py`:

```python
INSTALLED_APPS = [
    # ... apps padrão
    "rest_framework",
    "rest_framework.authtoken",
    "django_extensions",
    "products",
    "orders",
]

REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
}
```

### ETAPA 4 — Models Básicos

`products/models.py`

```python
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
```

`orders/models.py`

```python
from django.db import models
from django.contrib.auth.models import User
from products.models import Product

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
```

### ETAPA 5 — Serializers e Views

`products/views.py`

```python
from rest_framework.viewsets import ModelViewSet
from .models import Product
from .serializers import ProductSerializer

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
```

### ETAPA 6 — URLs

`core/urls.py`

```python
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from products.views import ProductViewSet
from orders.views import OrderViewSet

router = DefaultRouter()
router.register(r"products", ProductViewSet)
router.register(r"orders", OrderViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include(router.urls)),
]
```

### ETAPA 7 — Testes com Pytest + factory_boy + Faker

`products/tests/factories.py`

```python
import factory
from faker import Faker
from products.models import Product

fake = Faker()

class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product
    name = factory.LazyAttribute(lambda _: fake.word())
```

### ETAPA 8 — Makefile Básico

```makefile
# Makefile
run:
	docker-compose exec web python manage.py runserver

migrate:
	docker-compose exec web python manage.py migrate

lint:
	docker-compose exec web poetry run black .
	docker-compose exec web poetry run isort .

test:
	docker-compose exec web poetry run pytest -v
```

### ETAPA 9 — Docker + Docker Compose

`Dockerfile`

```dockerfile
FROM python:3.13-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Instala Poetry e dependências
COPY pyproject.toml poetry.lock ./
RUN pip install poetry && poetry install --no-root --no-dev

# Copia o código da aplicação
COPY . .
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

`docker-compose.yml`

```yaml
version: "3.9"
services:
  db:
    image: postgres:16-alpine
    environment:
      - POSTGRES_DB=BackendTemplate_dev_db
      - POSTGRES_USER=BackendTemplate_dev
      - POSTGRES_PASSWORD=BackendTemplate123
    volumes:
      - postgres_data:/var/lib/postgresql/data
  web:
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    depends_on:
      - db
    env_file:
      - .env
volumes:
  postgres_data:
```

### ETAPA 10 — GitHub Actions

`.github/workflows/main.yml`

```yaml
name: Django CI

on:
  push:
    branches: ["main"]
  pull_request:
    branches: ["main"]

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16-alpine
        env:
          POSTGRES_DB: test_db
          POSTGRES_USER: test_user
          POSTGRES_PASSWORD: test_password
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - name: 1. Checkout Repository
        uses: actions/checkout@v4

      - name: 2. Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.13"

      - name: 3. Install Poetry
        run: pip install poetry

      - name: 4. Configure Poetry
        run: poetry config virtualenvs.create false

      - name: 5. Install Dependencies
        run: poetry install --no-root -v

      - name: 6. Run Linters
        run: |
          poetry run black . --check
          poetry run isort . --check-only
          poetry run flake8 .

      - name: 7. Run Tests
        env:
          SQL_ENGINE: django.db.backends.postgresql
          SQL_DATABASE: test_db
          SQL_USER: test_user
          SQL_PASSWORD: test_password
          SQL_HOST: localhost
          SQL_PORT: 5432
          SECRET_KEY: a-test-secret-key-for-ci
          DEBUG: "1"
        run: poetry run pytest
```

## 👤 Autor

Feito com 💙 por [Renato Minoita](https://www.linkedin.com/in/renato-minoita/)

Confira mais no [GitHub](https://github.com/RNT13)
