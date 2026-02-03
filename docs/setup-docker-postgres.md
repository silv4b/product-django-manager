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
version: '3.8'

services:
  db:
    image: postgres:15
    container_name: postgres_db
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    environment:
      - POSTGRES_DB=basecoat_db
      - POSTGRES_USER=basecoat_user
      - POSTGRES_PASSWORD=basecoat_pass
    ports:
      - "5432:5432"

volumes:
  postgres_data:
```

## 3. Configuração de Variáveis de Ambiente

Para manter a segurança e facilitar a alteração de ambientes, é recomendável usar um arquivo `.env`.

Na raiz do projeto, crie um arquivo chamado `.env` e adicione as seguintes informações (correspondentes ao que definimos no docker-compose):

```env
DB_NAME=basecoat_db
DB_USER=basecoat_user
DB_PASSWORD=basecoat_pass
DB_HOST=localhost
DB_PORT=5432
```

## 4. Atualização das Configurações do Django

Agora você precisa alterar o arquivo `basecoat_project/settings.py` para que ele leia as informações do banco de dados a partir das variáveis de ambiente.

Primeiro, instale o pacote `python-dotenv` para permitir que o Django leia o arquivo `.env`:

```bash
pip install python-dotenv
```

Em seguida, abra o arquivo `basecoat_project/settings.py` e adicione no topo do arquivo (após os imports):

```python
import os
from dotenv import load_dotenv

load_dotenv()
```

E altere a seção `DATABASES` para:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}
```

## 5. Execução do Banco de Dados

Com tudo configurado, você pode subir o contêiner do PostgreSQL. Abra o terminal na raiz do projeto e execute:

```bash
docker-compose up -d
```

O comando `-d` serve para rodar o processo em segundo plano (detached mode).

Para verificar se o contêiner está rodando:

```bash
docker ps
```

## 6. Realização das Migrações

Agora que o banco de dados PostgreSQL está ativo e o Django está apontando para ele, você precisa criar a estrutura das tabelas:

```bash
python manage.py migrate
```

## 7. Comandos Úteis para o Dia a Dia

Para parar o banco de dados:

```bash
docker-compose stop
```

Para iniciar novamente:

```bash
docker-compose start
```

Para remover o contêiner (os dados serão mantidos no volume):

```bash
docker-compose down
```

Para visualizar os logs em tempo real caso ocorra algum erro:

```bash
docker-compose logs -f
```
