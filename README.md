# Backend API de Vendas 🐍

Um template profissional de backend usando **Django**, **Django REST
Framework**, **Poetry**, **Docker**, **PostgreSQL**, CI com **GitHub
Actions**, e suporte para deploy em **Render**.

Este README combina as instruções originais com o guia completo de
criação de projetos usando Poetry, GitHub e Render.

---

## 📖 Índice

1.  ✅ Como Usar o Projeto (Guia Rápido)
2.  ✅ Como Construir Este Projeto do Zero (Tutorial)
3.  ✅ Preparando para Deploy no Render
4.  ✅ Comandos Úteis (Docker, Makefile, Poetry)
5.  ✅ Autor

---

# ✅ 1. Como Usar o Projeto (Guia Rápido)

### ✅ Clonar o Projeto

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

---

### ✅ Configurar o Arquivo `.env`

Crie um arquivo `.env` com:

```env
DEBUG=1
SECRET_KEY=sua-chave-secreta
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1

SQL_ENGINE=django.db.backends.postgresql
SQL_DATABASE=BackendTemplate_dev_db
SQL_USER=BackendTemplate_dev
SQL_PASSWORD=BackendTemplate123
SQL_HOST=db
SQL_PORT=5432
```

---

### ✅ Subir os Containers com Docker

```bash
docker-compose up -d --build
```

Acesse: http://localhost:8000

---

### ✅ Aplicar Migrações e Criar Superusuário

```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

---

### ✅ Endpoints Principais

---

Método Endpoint Descrição

---

GET/POST /api/v1/products/ Lista ou cria produtos

GET/PUT/DELETE /api/v1/products/{id}/ Detalha/edita/deleta
produto

GET/POST /api/v1/orders/ Lista ou cria pedidos

GET /api/v1/orders/{id}/ Detalha pedido

---

---

### ✅ Testes e Qualidade

```bash
docker-compose exec web poetry run pytest -v
docker-compose exec web poetry run black .
docker-compose exec web poetry run isort .
docker-compose exec web poetry run flake8 .
```

---

# ✅ 2. Como Construir Este Projeto do Zero (Tutorial)

### 🧩 Criar Projeto com Poetry

```bash
poetry init -n
poetry add django djangorestframework psycopg2-binary django-extensions
poetry add black isort flake8 pytest pytest-django factory-boy faker --group dev
```

---

### 🏗️ Criar Estrutura Django

```bash
poetry run django-admin startproject core .
poetry run python manage.py startapp products
poetry run python manage.py startapp orders
```

---

### 🛠️ Configurações do Django

Adicionar em `core/settings.py`:

```python
INSTALLED_APPS = [
    "rest_framework",
    "rest_framework.authtoken",
    "django_extensions",
    "products",
    "orders",
]
```

---

### 📦 Models de Exemplo

`products/models.py`

```python
class Product(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
```

---

### 🔄 URLs

`core/urls.py`:

```python
router.register(r"products", ProductViewSet)
router.register(r"orders", OrderViewSet)
```

---

# ✅ 3. Deploy no Render

Render exige `requirements.txt`.

### ✅Com poetry gerar requirements.txt:

```bash
poetry export -f requirements.txt --output requirements.txt --without-hashes
```

### ✅Com pip gerar requirements.txt:

```bash
pip freeze > requirements.txt

```

### ✅ Instalar pacotes para Deploy

```bash
poetry add gunicorn psycopg2-binary dj-database-url
poetry export -f requirements.txt --output requirements.txt --without-hashes
```

---

### ✅ Configurações extras no Django

`settings.py`:

```python
import dj_database_url

DATABASES = {
    'default': dj_database_url.config(default='sqlite:///db.sqlite3')
}

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
ALLOWED_HOSTS = ["*"]
```

---

### ✅ Procfile

    web: gunicorn core.wsgi:application

---

### ✅ render.yaml

```yaml
services:
  - type: web
    name: backend-api
    runtime: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn core.wsgi:application
```

---

# ✅ 4. Comandos Úteis

### ✅ Makefile:

Comando Ação

---

make up Sobe Docker
make down Para os containers
make logs Logs
make migrate Migrações
make test Roda testes
make lint Verifica código
make format Formata código

---

### ✅ Poetry

Comando Ação

---

poetry install Instala dependências
poetry add x Adiciona pacote
poetry shell Entra no ambiente
poetry run x Executa comando

---

# 👤 Autor

**Renato Minoita**\
GitHub: https://github.com/RNT13\
LinkedIn: https://www.linkedin.com/in/renato-minoita/
