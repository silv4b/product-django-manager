# Kore Product Manager

O Kore é um sistema de gerenciamento de inventário de produtos moderno, construído com foco em experiência do usuário, criado para testar o uso do Basecoat UI em um projeto Django.

## Tecnologias

O projeto utiliza as seguintes tecnologias:

- Backend: [Python](https://www.python.org/) 3.10+ [Django](https://www.djangoproject.com/) 6.0+
- Frontend: HTML5, JavaScript (Vanilla)
- API: [Django Rest Framework](https://www.django-rest-framework.org/), [SimpleJWT](https://django-rest-framework-simplejwt.readthedocs.io/), [drf-spectacular](https://drf-spectacular.readthedocs.io/)
- Estilização: [Tailwind CSS](https://tailwindcss.com/) v4.0+
- UI Framework: [Basecoat UI](https://basecoatui.com/)
- Autenticação: [Django Allauth](https://docs.allauth.org/en/latest/) e JWT para API
- Banco de Dados: [SQLite3](https://sqlite.org/) ou [PostgreSQL](https://www.postgresql.org/)
- Ícones: [Lucide Icons](https://lucide.dev/) (via CDN)

## Funcionalidades Principais

- Gestão de Produtos: CRUD completo (Criação, Visualização, Edição e Exclusão) de produtos.
- Dashboard de Estoque: Histórico de movimentações (Entradas/Saídas) com estatísticas detalhadas.
- Painel de Controle: Alternância entre modos de visualização (Grade e Tabela) persistente por usuário.
- Histórico de Preços: Rastreamento automático de mudanças de preço com visualização em gráfico (sparkline).
- API REST: Endpoints para integração com outras aplicações, incluindo documentação Swagger e ReDoc.
- Visibilidade de Produtos: Suporte para produtos públicos (catálogo global) e privados (visíveis apenas pelo dono).
- Sistema de Notificações: Toasts globais para feedback em tempo real das ações do usuário.
- Segurança do Usuário:
  - Validação de força de senha em tempo real no cadastro e alteração.
  - Alternância de visibilidade de senha (mostrar/esconder).
  - Gerenciamento de perfil e exclusão permanente de conta.
- Interface Adaptativa: Modo Escuro (Dark Mode) e Modo Claro inteligente com alternância fluida.

## Como Executar o Projeto

### Pré-requisitos

- [uv](https://docs.astral.sh/uv/) (gerenciador de pacotes e ambientes Python).
  - `pip install uv` ou [chaque a documentação](https://docs.astral.sh/uv/getting-started/installation/).
- Node.js (para compilação do CSS).

### Passos para Instalação

1. Clone o repositório para sua máquina local.

2. Instale as dependências do Python:
   `uv sync`

3. Instale as dependências do Node.js:
   `npm install`

4. Configure as variáveis de ambiente (Opcional):
   Crie um arquivo `.env` baseado no `.env.example`. Se não configurado, o sistema usará SQLite por padrão.

5. Execute as migrações do banco de dados:
   `uv run manage.py migrate`

### Executando a Aplicação

Para rodar o projeto, você precisará de dois processos rodando (ou buildar o CSS antes):

1. Compilação do Tailwind CSS (em um terminal):
   `npm run watch`

   (Ou para build de produção: `npm run build`)

2. Servidor de Desenvolvimento (em outro terminal):
   `uv run manage.py runserver`

A aplicação estará disponível em: <http://127.0.0.1:8000/>

### Acessando a API

A API REST está disponível no prefixo `/api/v1/`.
Para documentação interativa, acesse:

- **Swagger UI**: <http://127.0.0.1:8000/api/v1/docs/swagger/>
- **ReDoc**: <http://127.0.0.1:8000/api/v1/docs/redoc/>

## Documentação Adicional

Para mais guias e configurações, consulte a pasta `docs/`:

- [Guia de Configuração do Ambiente de Desenvolvimento](docs/setup-ambiente-desenvolvimento.md)
- [Validação de E-mail com Django-Allauth](docs/django-allauth-email-validation.md)
- [Login Social (Google e GitHub) com Django-Allauth](docs/django-allauth-social-login.md)
- [Configuração Docker e PostgreSQL](docs/setup-docker-postgres.md)
- [Uso de UV e PoeThePoet](docs/uv-and-poethepoet.md)
- [Roadmap do Projeto](docs/kore-product-roadmap.md)
