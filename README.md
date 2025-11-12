# Backend API de Vendas 🐍

Um template profissional de backend usando **Django**, **Django REST Framework**, **Poetry**, **Docker**, **PostgreSQL**, CI com **GitHub Actions**, e suporte para deploy em **Render**.

Este README é um guia completo, desde a configuração inicial até o deploy, explicando os conceitos-chave para desenvolvimento local e em produção.

---

## 📖 Índice

1.  [**Conceitos Essenciais**](#-1-conceitos-essenciais)
    - [Gerenciamento de Ambiente com `.env`](#-gerenciamento-de-ambiente-com-env)
    - [Desenvolvimento com Docker](#-desenvolvimento-com-docker)
2.  [**Como Usar o Projeto (Guia Rápido)**](#-2-como-usar-o-projeto-guia-rápido)
    - [Desenvolvimento Local (Recomendado)](#-desenvolvimento-local-recomendado)
    - [Desenvolvimento via Docker Compose](#-desenvolvimento-via-docker-compose)
3.  [**Comandos Úteis**](#-3-comandos-úteis)
4.  [**Deploy no Render**](#-4-deploy-no-render)
5.  [**Como Construir Este Projeto do Zero**](#-5-como-construir-este-projeto-do-zero)
6.  [**Autor**](#-6-autor)

---

# ✅ 1. Conceitos Essenciais

Antes de iniciar, entenda os dois pilares do ambiente de desenvolvimento deste projeto.

### 📋 Gerenciamento de Ambiente com `.env`

Este projeto utiliza um arquivo `.env` para gerenciar configurações sensíveis e específicas de cada ambiente (local, Docker, produção), sem expô-las no código-fonte.

**Por que usar `.env`?**

- **Segurança:** Mantém chaves de API, senhas de banco de dados e `SECRET_KEY` fora do Git.
- **Flexibilidade:** Permite que cada desenvolvedor use configurações locais diferentes sem alterar o código.
- **Padrão de Mercado:** É a abordagem padrão em projetos modernos.

**Como funciona?**
A biblioteca `python-dotenv` carrega as variáveis de um arquivo `.env` e o `settings.py` as utiliza para configurar o Django.

**Existem dois modos de configuração neste projeto:**

1.  **Para desenvolvimento local (`python manage.py runserver`):** O Django precisa se conectar ao banco de dados Docker via `localhost`.
2.  **Para desenvolvimento com Docker (`docker-compose up`):** O contêiner do Django se conecta ao contêiner do banco de dados usando o nome do serviço (`db`).

O arquivo `.env` correto para cada cenário é crucial.

### 🐳 Desenvolvimento com Docker

Docker containeriza a aplicação, garantindo que ela rode da mesma forma em qualquer máquina.

**Principais Arquivos:**

- `Dockerfile`: A "receita" para construir a imagem da nossa aplicação Django. Define o sistema operacional, instala dependências e configura como a aplicação deve ser executada.
- `docker-compose.yml`: Orquestra múltiplos contêineres. Neste projeto, ele gerencia o contêiner da aplicação (`web`) e o do banco de dados (`db`), além de configurar a rede entre eles, volumes e portas.
- `.dockerignore`: Similar ao `.gitignore`, especifica arquivos e pastas que devem ser ignorados ao construir a imagem, tornando-a mais leve e segura (ex: `.venv`, `__pycache__`).

**Como Atualizar sua Imagem no Docker Hub:**
Para publicar uma nova versão da sua imagem (`renatornt13/backend-template`):

```bash
# 1. Faça login no Docker Hub
docker login

# 2. Construa a nova imagem
docker build -t renatornt13/backend-template .

# 3. Adicione uma tag de versão (boa prática)
docker tag renatornt13/backend-template:latest renatornt13/backend-template:v1.1

# 4. Envie a nova versão para o Docker Hub
docker push renatornt13/backend-template:v1.1

# 5. (Opcional) Atualize também a tag 'latest'
docker push renatornt13/backend-template:latest
```

---

# ✅ 2. Como Usar o Projeto (Guia Rápido)

Existem duas maneiras de rodar este projeto. O método local é mais rápido para o dia a dia.

### 💻 Desenvolvimento Local (Recomendado)

Neste modo, você roda o Django diretamente na sua máquina, mas se conecta ao banco de dados que está no Docker.

**1. Clone o Projeto:**

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

**2. Inicie o Banco de Dados com Docker:**

```bash
docker-compose up -d db
```

**3. Crie o Arquivo `.env` para o Ambiente Local:**
Crie um arquivo chamado `.env` na raiz do projeto com o seguinte conteúdo. **Atenção ao `SQL_HOST` e `SQL_PORT`!**

```env
# Configurações para desenvolvimento local
DEBUG=1
SECRET_KEY=django-insecure-local-secret-key
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# Conexão com o banco de dados Docker a partir da sua máquina
SQL_HOST=localhost
SQL_PORT=5433 # Porta exposta no docker-compose.yml

# Credenciais do banco de dados
SQL_DATABASE=BackendTemplate_dev_db
SQL_USER=BackendTemplate_dev
SQL_PASSWORD=BackendTemplate123
```

**4. Instale as Dependências e Ative o Ambiente com Poetry:**

```bash
# Instala dependências e cria o .venv
poetry install

# Ativa o ambiente no terminal
poetry env activate

# Depois use o comando que será explicado abaixo, exemplo:
& "D:\Curso\MeusProjetos (Python)\Backend-template\.venv\Scripts\activate.ps1"
```

**5. Aplique as Migrações e Crie um Usuário:**

```bash
python manage.py migrate
python manage.py createsuperuser
```

**6. Rode o Servidor:**

```bash
python manage.py runserver
```

Acesse: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

### 🐳 Desenvolvimento via Docker Compose

Neste modo, tanto o Django quanto o banco de dados rodam dentro de contêineres.

**1. Clone o Projeto.**

**2. Crie o Arquivo `.env` para o Ambiente Docker:**
Crie um arquivo `.env` com o conteúdo abaixo. **Note que `SQL_HOST` agora é `db`**.

```env
# Configurações para o ambiente Docker
DEBUG=1
SECRET_KEY=django-insecure-docker-secret-key
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# Conexão entre contêineres
SQL_HOST=db
SQL_PORT=5432 # Porta interna da rede Docker

# Credenciais
SQL_DATABASE=BackendTemplate_dev_db
SQL_USER=BackendTemplate_dev
SQL_PASSWORD=BackendTemplate123
```

**3. Suba os Contêineres:**

```bash
docker-compose up -d --build
```

**4. Aplique as Migrações e Crie um Usuário:**

```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

Acesse: [http://localhost:8000](http://localhost:8000)

---

# ✅ 3. Comandos Úteis

### ✅ Makefile

Use `make` para simplificar os comandos Docker.

| Comando        | Ação                                          |
| -------------- | --------------------------------------------- |
| `make up`      | Sobe os contêineres Docker em modo detached   |
| `make down`    | Para e remove os contêineres                  |
| `make logs`    | Exibe os logs dos contêineres                 |
| `make migrate` | Aplica as migrações dentro do contêiner `web` |
| `make test`    | Roda os testes com Pytest                     |
| `make lint`    | Verifica o código com Flake8                  |
| `make format`  | Formata o código com Black e isort            |

### ✅ Poetry

| Comando               | Ação                                              |
| --------------------- | ------------------------------------------------- |
| `poetry install`      | Instala todas as dependências do `pyproject.toml` |
| `poetry add <pacote>` | Adiciona um novo pacote ao projeto                |
| `poetry shell`        | Ativa o ambiente virtual no shell atual           |
| `poetry run <cmd>`    | Executa um comando dentro do ambiente virtual     |

---

# ✅ 4. Deploy no Render

O projeto está pré-configurado para deploy no Render.

**1. Gere o `requirements.txt`:**
O Render usa `requirements.txt`. Gere-o a partir do `poetry.lock`:

```bash
pip freeze > requirements.txt
```

**2. Faça o Push para o GitHub:**
Garanta que seu `requirements.txt` esteja atualizado no seu repositório.

**3. Deploy no Render**

O projeto está **totalmente preparado para deploy no Render**, com configuração automática para detectar o ambiente de produção e ajustar o comportamento do Django de forma segura.

### ⚙️ Configuração do Ambiente

O `settings.py` identifica automaticamente o ambiente Render:

```python
IS_RENDER = os.getenv("RENDER", "false").lower() == "true"
DEBUG = bool(int(os.getenv("DEBUG", 1))) if not IS_RENDER else False
ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "127.0.0.1 localhost").split()
if IS_RENDER:
    RENDER_EXTERNAL_HOSTNAME = os.getenv("RENDER_EXTERNAL_HOSTNAME")
    if RENDER_EXTERNAL_HOSTNAME:
        ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)
```

🔍 **Explicação:**

- O Render define `RENDER=true`, e o Django ajusta `DEBUG=False` automaticamente.
- O domínio público do Render é adicionado automaticamente ao `ALLOWED_HOSTS`.
- Caso ocorra o erro **400 Bad Request**, adicione temporariamente `ALLOWED_HOSTS=["*"]`.

---

### 🧱 Passos para o Deploy

1. **Gerar o `requirements.txt`:**

```bash
pip freeze > requirements.txt
```

2. **Fazer o Push para o GitHub.**

3. **Criar o serviço no Render:**

   - **Build Command:**
     ```bash
     pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput
     ```
   - **Start Command:**
     ```bash
     gunicorn core.wsgi:application
     ```

4. **Variáveis de ambiente no Render:**

| Variável               | Valor                               |
| ---------------------- | ----------------------------------- |
| `RENDER`               | `true`                              |
| `DATABASE_URL`         | Internal Database URL do PostgreSQL |
| `SECRET_KEY`           | Chave gerada pelo Django            |
| `DEBUG`                | `0`                                 |
| `DJANGO_ALLOWED_HOSTS` | (opcional) domínio do Render        |

---

### 🚀 Evitando Erro 400

Se aparecer **Bad Request (400)**, adicione o domínio do Render manualmente nas variáveis de ambiente:

```bash
DJANGO_ALLOWED_HOSTS=backend-django-xyz.onrender.com
```

E reinicie o serviço.

---

### 🧩 Boas Práticas

- ✅ Nunca use `DEBUG=True` em produção.
- ✅ Use `RENDER=true` para ativar o modo de produção.
- ✅ Utilize a **Internal Database URL** no `DATABASE_URL`.
- ✅ Prefira manter `ALLOWED_HOSTS` dinâmico.

---

# ✅ 5. Como Construir Este Projeto do Zero (Tutorial)

Este guia detalha o processo de criação deste template do zero, explicando as decisões de arquitetura e as melhores práticas adotadas.

### Passo 1: Inicializar o Projeto com Poetry

Poetry é a ferramenta escolhida para gerenciar dependências e ambientes virtuais, garantindo reprodutibilidade.

1.  **Crie a pasta do projeto e inicie o Poetry:**

    ```bash
    mkdir backend-template
    cd backend-template
    poetry init -n
    ```

    - O comando `init -n` cria um `pyproject.toml` básico sem fazer perguntas.

2.  **Adicione as dependências principais:**

    ```bash
    poetry add django djangorestframework psycopg2-binary django-extensions dj-database-url python-dotenv
    ```

    - `django` e `djangorestframework`: O coração do projeto.
    - `psycopg2-binary`: Adaptador para o banco de dados PostgreSQL.
    - `django-extensions`: Fornece ferramentas úteis de desenvolvimento.
    - `dj-database-url` e `python-dotenv`: Para gerenciar a configuração do banco de dados a partir de variáveis de ambiente.

3.  **Adicione as dependências de desenvolvimento:**
    ```bash
    poetry add black isort flake8 pytest pytest-django --group dev
    ```
    - `--group dev` separa as ferramentas de qualidade de código e testes das dependências de produção.

### Passo 2: Estrutura Inicial do Django

Com o ambiente pronto, criamos a estrutura base do Django.

1.  **Crie o projeto principal e os apps:**

    ```bash
    # Cria o projeto 'core' no diretório atual (.)
    poetry run django-admin startproject core .

    # Cria os apps de exemplo
    poetry run python manage.py startapp products
    poetry run python manage.py startapp orders
    ```

2.  **Configure o `settings.py`:**
    Abra `core/settings.py` e adicione os novos apps a `INSTALLED_APPS`:
    ```python
    INSTALLED_APPS = [
        # ... apps padrão do Django ...
        "rest_framework",
        "rest_framework.authtoken",
        "django_extensions",
        "products",
        "orders",
    ]
    ```

### Passo 3: Configurar o Ambiente Docker

Docker garante que o ambiente de desenvolvimento seja idêntico para todos.

1.  **Crie o `Dockerfile`:**
    Este arquivo define como construir a imagem da nossa aplicação.

    ```Dockerfile
    # Use uma imagem Python leve
    FROM python:3.13-slim

    # Evita que o Python gere arquivos .pyc e armazene logs em buffer
    ENV PYTHONDONTWRITEBYTECODE 1
    ENV PYTHONUNBUFFERED 1

    WORKDIR /app

    # Instala o Poetry
    RUN pip install poetry

    # Copia os arquivos de dependência e desativa a criação de .venv pelo Poetry
    COPY pyproject.toml poetry.lock* ./
    RUN poetry config virtualenvs.create false && poetry install --no-root --no-dev

    # Copia o restante do código da aplicação
    COPY . .

    # Expõe a porta que a aplicação irá rodar
    EXPOSE 8000
    ```

2.  **Crie o `docker-compose.yml`:**
    Este arquivo orquestra os serviços da aplicação (web e banco de dados).

    ```yaml
    version: "3.8"

    services:
      db:
        image: postgres:16-alpine
        container_name: backend-template-db
        volumes:
          - postgres_data:/var/lib/postgresql/data
        ports:
          - "5433:5432"
        environment:
          - POSTGRES_USER=BackendTemplate_dev
          - POSTGRES_PASSWORD=BackendTemplate123
          - POSTGRES_DB=BackendTemplate_dev_db

      web:
        build: .
        container_name: backend-template-web
        command: python manage.py runserver 0.0.0.0:8000
        volumes:
          - .:/app
        ports:
          - "8000:8000"
        env_file:
          - .env
        depends_on:
          - db

    volumes:
      postgres_data:
    ```

3.  **Crie o `.dockerignore`:**
    Para manter a imagem Docker limpa e leve.
    ```
    .git
    .venv
    __pycache__
    db.sqlite3
    *.pyc
    ```

### Passo 4: Finalizar a Configuração do Django

Agora, conectamos o Django ao Docker e às variáveis de ambiente.

1.  **Ajuste o `settings.py` para usar variáveis de ambiente:**
    Modifique a seção `DATABASES` em `core/settings.py` para ler as configurações do `.env`, como mostrado na seção de **Conceitos Essenciais**. Isso permite que o Django se conecte tanto a `localhost:5433` (localmente) quanto a `db:5432` (via Docker).

2.  **Crie os arquivos `.env`:**
    Crie os dois arquivos `.env` (um para desenvolvimento local e outro para Docker) conforme explicado na seção **Como Usar o Projeto**.

### Passo 5: Rodar e Testar

Com tudo configurado, seu ambiente está pronto.

1.  **Suba os contêineres:**

    ```bash
    docker-compose up -d --build
    ```

2.  **Execute as migrações:**
    ```bash
    docker-compose exec web python manage.py migrate
    ```

Seu projeto-template agora está totalmente funcional, seguindo as melhores práticas de desenvolvimento, gerenciamento de dependências e containerização.

---

# 👤 6. Autor

**Renato Minoita**

- GitHub: [https://github.com/RNT13](https://github.com/RNT13)
- LinkedIn: [https://www.linkedin.com/in/renato-minoita/](https://www.linkedin.com/in/renato-minoita/)
