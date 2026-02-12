# Kore Product Manager API

Esta é a API REST para o sistema Kore Product Manager.

## Autenticação

A API utiliza **JWT (JSON Web Token)** para autenticação.

1. **Obter Token**: Envie uma requisição `POST` para `/api/v1/token/` com `username` e `password`.
2. **Usar Token**: Inclua o token no cabeçalho das requisições: `Authorization: Bearer <seu_token_access>`.
3. **Atualizar Token**: Use `/api/v1/token/refresh/` quando o token de acesso expirar.

## Endpoints Principais

- `GET /api/v1/products/`: Lista produtos do usuário logado.
- `POST /api/v1/products/`: Cria um novo produto.
- `GET /api/v1/products/{id}/`: Detalhes do produto (inclui histórico de preços e movimentações).
- `POST /api/v1/products/{id}/movement/`: Registra uma entrada (`IN`) ou saída (`OUT`) de estoque.
- `GET /api/v1/categories/`: Lista e gerencia categorias.
- `GET /api/v1/movements/`: Histórico unificado de movimentações.

## Documentação Interativa

A documentação completa dos endpoints, esquemas e parâmetros está disponível em:

- **Swagger UI**: `/api/v1/docs/swagger/`
- **ReDoc**: `/api/v1/docs/redoc/`

## Tecnologias Utilizadas

- Django Rest Framework
- SimpleJWT (Autenticação)
- drf-spectacular (Documentação OpenAPI 3.0)
- django-filter (Filtragem dinâmica)
