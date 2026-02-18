# Guia de Configuração do PostgreSQL com Docker e Docker Compose

Este documento fornece o passo a passo para configurar um banco de dados PostgreSQL utilizando Docker dentro do seu projeto Django no ambiente Windows.

## 1. Instalação do Docker Desktop

Antes de começar a configurar o projeto, você precisa ter o Docker instalado no seu Windows.

1. Acesse o site oficial do [Docker Desktop](https://www.docker.com/products/docker-desktop/).
2. Clique no botão de download para Windows.
3. Execute o instalador e siga as instruções na tela. Certifique-se de que a opção "Use the WSL 2 based engine" esteja marcada (recomendado para melhor performance no Windows).
4. Após o término, reinicie o computador se solicitado.
5. Abra o Docker Desktop e aguarde até que o ícone no canto inferior indique que o Docker está em execução.

## 2. Criação do arquivo docker-compose.yml

Na raiz do seu projeto, crie um arquivo chamado `docker-compose.yml`. Este arquivo define como o contêiner do PostgreSQL deve ser construído e executado.

Crie o arquivo com o seguinte conteúdo:

```yaml
services:
  db:
    image: postgres:15
    container_name: postgres_db
    restart: always
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    environment:
      - POSTGRES_PASSWORD=basecoat_pass
    ports:
      - "5432:5432"

volumes:
  postgres_data:
```

## 3. Configuração de Variáveis de Ambiente

Para manter a segurança e facilitar a alteração de ambientes, é recomendável usar um arquivo `.env`.

Na raiz do projeto, crie um arquivo chamado `.env` (ou copie do `.env.example`) e adicione as seguintes informações:

```env
DB_NAME=basecoat_db
DB_USER=basecoat_user
DB_PASSWORD=basecoat_pass
DB_HOST=localhost
DB_PORT=5432
```

## 4. Instalação das Dependências

Para que o Django consiga se comunicar com o PostgreSQL e ler o arquivo `.env`, você precisa instalar os pacotes necessários utilizando o `uv`:

```bash
uv add psycopg2-binary python-dotenv
```

*Nota: O `psycopg2-binary` é o adaptador do banco de dados e o `python-dotenv` é usado para carregar as variáveis do arquivo `.env`.*

## 5. Verificação das Configurações do Django

O projeto já vem configurado para buscar essas variáveis de ambiente. Verifique o arquivo `kore-product-manager/settings.py` para garantir que as seções abaixo estejam presentes.

No topo do arquivo (após os imports):

```python
from pathlib import Path
import os
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

# Carrega variáveis do arquivo .env
load_dotenv(BASE_DIR / ".env")
```

E a seção `DATABASES`:

```python
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_PORT = os.environ.get("DB_PORT", "5432")

if DB_NAME and DB_USER and DB_PASSWORD:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": DB_NAME,
            "USER": DB_USER,
            "PASSWORD": DB_PASSWORD,
            "HOST": DB_HOST,
            "PORT": DB_PORT,
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
```

## 6. Execução do Banco de Dados

Com tudo configurado, você pode subir o contêiner do PostgreSQL. Abra o terminal na raiz do projeto e execute:

```bash
docker compose up -d
```

O comando `-d` serve para rodar o processo em segundo plano (detached mode).

Para verificar se o contêiner está rodando:

```bash
docker ps
```

## 7. Realização das Migrações

Agora que o banco de dados PostgreSQL está ativo e o Django está configurado para usá-lo, você precisa criar a estrutura das tabelas:

```bash
uv run manage.py migrate
```

## 8. Comandos Úteis para o Dia a Dia

Para parar o banco de dados:

```bash
docker compose stop
```

Para iniciar novamente:

```bash
docker compose start
```

Para remover o contêiner (os dados serão mantidos no volume):

```bash
docker compose down
```

Para visualizar os logs em tempo real:

```bash
docker compose logs -f
```
