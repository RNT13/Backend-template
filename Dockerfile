FROM python:3.13-slim

# Configurações básicas
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Instalar dependências de sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && apt-get clean

# Instalar dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o projeto
COPY . .

# Variáveis para o Render
ENV DJANGO_SETTINGS_MODULE=core.settings
ENV PORT=8000

# Coletar arquivos estáticos
RUN python manage.py collectstatic --noinput

EXPOSE 8000

# Rodar Gunicorn em produção
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]
