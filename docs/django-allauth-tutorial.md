# Tutorial: Sistema de Autenticação com Django e django-allauth

Este tutorial guiado ensina como criar um sistema completo de autenticação do zero usando **Django** e **django-allauth**, cobrriendo: login, criar conta, alterar senha (logado) e recuperar senha.

---

## 1. Visão Geral

O **django-allauth** é uma biblioteca Django que fornece uma solução completa de autenticação, incluindo:
- Login/Logout
- Cadastro de usuários (signup)
- Recuperação de senha (password reset)
- Alteração de senha
- Login social (Google, Facebook, etc.)
- Verificação de email

Este tutorial usa a versão do Django 6.x e django-allauth 65.x.

---

## 2. Pré-requisitos

Antes de começar, certifique-se de ter:

- **Python 3.14+** instalado
- **UV** (gerenciador de pacotes) instalado
- **Node.js & npm** (para frontend)
- Conhecimento básico de Django

Consulte o guia de [setup do ambiente de desenvolvimento](./setup-ambiente-desenvolvimento.md) para instruções de instalação.

---

## 3. Criando o Projeto do Zero

### 3.1 Criar novo projeto Django

```bash
# Criar novo projeto
django-admin startproject meuprojeto
cd meuprojeto

# Criar app para contas
python manage.py startapp accounts
```

### 3.2 Estrutura de pastas

Após a criação, sua estrutura deve ficar assim:

```
meuprojeto/
├── manage.py
├── meuprojeto/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── accounts/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
└── templates/        # Criar esta pasta
    └── base.html
```

---

## 4. Configuração do settings.py

Abra o arquivo `meuprojeto/settings.py` e faça as seguintes alterações:

### 4.1 Adicionar apps instalados

Encontre a lista `INSTALLED_APPS` e adicione:

```python
INSTALLED_APPS = [
    # ... apps existentes
    'django.contrib.sites',           # Obrigatório para allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'accounts',                        # Seu app de contas
]
```

### 4.2 Adicionar Authentication Backends

Adicione após `USE_TZ = True`:

```python
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

SITE_ID = 1
```

### 4.3 Configurar redirects

Adicione estas linhas:

```python
# Redirects
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/accounts/login/'
ACCOUNT_LOGIN_REDIRECT_URL = '/'
ACCOUNT_LOGOUT_REDIRECT_URL = '/accounts/login/'
```

### 4.4 Configurações do allauth

Adicione estas configurações:

```python
# Configurações do django-allauth
ACCOUNT_EMAIL_VERIFICATION = 'none'  # 'none', 'optional', 'mandatory'
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_SIGNUP_FIELDS = ['email*', 'username*', 'password1*', 'password2*']
```

### 4.5 Configurar diretório de templates

No bloco `TEMPLATES`, certifique-se de incluir a pasta `templates`:

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        # ...
    },
]
```

---

## 5. Configuração de URLs

### 5.1 URLs principais

Abra `meuprojeto/urls.py` e adicione:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('accounts.urls')),  # Suas URLs personalizadas
]
```

### 5.2 URLs do allauth (disponíveis automaticamente)

| Funcionalidade | URL |
|----------------|-----|
| Login | `/accounts/login/` |
| Criar Conta | `/accounts/signup/` |
| Logout | `/accounts/logout/` |
| Alterar Senha | `/accounts/password/change/` |
| Esqueceu Senha | `/accounts/password/reset/` |
| Confirmar Email | `/accounts/confirm-email/` |

---

## 6. Criando os Templates

### 6.1 Estrutura de pastas

Crie a seguinte estrutura dentro da pasta `templates/`:

```
templates/
├── base.html
└── account/
    ├── login.html
    ├── signup.html
    ├── password_change.html
    ├── password_reset.html
    ├── password_reset_done.html
    ├── password_reset_from_key.html
    └── password_reset_from_key_done.html
```

### 6.2 base.html

```html
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Meu Projeto{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="/">Meu Projeto</a>
            <div class="navbar-nav ms-auto">
                {% if user.is_authenticated %}
                    <span class="nav-item nav-link">Olá, {{ user.username }}</span>
                    <a class="nav-item nav-link" href="{% url 'account_change_password' %}">Alterar Senha</a>
                    <form method="post" action="{% url 'account_logout' %}" class="d-inline">
                        {% csrf_token %}
                        <button type="submit" class="btn btn-link nav-item nav-link">Sair</button>
                    </form>
                {% else %}
                    <a class="nav-item nav-link" href="{% url 'account_login' %}">Login</a>
                    <a class="nav-item nav-link" href="{% url 'account_signup' %}">Cadastrar</a>
                {% endif %}
            </div>
        </div>
    </nav>
    
    <div class="container mt-4">
        {% if messages %}
            {% for message in messages %}
                <div class="alert alert-{{ message.tags }}">{{ message }}</div>
            {% endfor %}
        {% endif %}
        
        {% block content %}{% endblock %}
    </div>
</body>
</html>
```

### 6.3 account/login.html

```html
{% extends "base.html" %}
{% load allauth %}

{% block title %}Login{% endblock %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-md-6">
        <div class="card">
            <div class="card-header">
                <h3>Entrar</h3>
            </div>
            <div class="card-body">
                {% element form method="post" action="/accounts/login/" %}
                    {% csrf_token %}
                    {% slot body %}
                        {{ form.as_p }}
                        {% if redirect_field_value %}
                            <input type="hidden" name="{{ redirect_field_name }}" value="{{ redirect_field_value }}">
                        {% endif %}
                    {% endslot %}
                    {% slot actions %}
                        <button type="submit" class="btn btn-primary w-100">Entrar</button>
                    {% endslot %}
                {% endelement %}
                
                <div class="mt-3 text-center">
                    <a href="{% url 'account_signup' %}">Não tem conta? Cadastre-se</a><br>
                    <a href="{% url 'account_reset_password' %}">Esqueceu sua senha?</a>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

### 6.4 account/signup.html (Criar Conta)

```html
{% extends "base.html" %}
{% load allauth %}

{% block title %}Criar Conta{% endblock %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-md-6">
        <div class="card">
            <div class="card-header">
                <h3>Criar Nova Conta</h3>
            </div>
            <div class="card-body">
                {% element form method="post" action="/accounts/signup/" %}
                    {% csrf_token %}
                    {% slot body %}
                        {{ form.as_p }}
                        {% if redirect_field_value %}
                            <input type="hidden" name="{{ redirect_field_name }}" value="{{ redirect_field_value }}">
                        {% endif %}
                    {% endslot %}
                    {% slot actions %}
                        <button type="submit" class="btn btn-success w-100">Cadastrar</button>
                    {% endslot %}
                {% endelement %}
                
                <div class="mt-3 text-center">
                    <a href="{% url 'account_login' %}">Já tem conta? Entre</a>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

### 6.5 account/password_change.html (Alterar Senha - Logado)

```html
{% extends "base.html" %}
{% load allauth %}

{% block title %}Alterar Senha{% endblock %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-md-6">
        <div class="card">
            <div class="card-header">
                <h3>Alterar Senha</h3>
            </div>
            <div class="card-body">
                {% element form method="post" action="/accounts/password/change/" %}
                    {% csrf_token %}
                    {% slot body %}
                        {{ form.as_p }}
                        {% if redirect_field_value %}
                            <input type="hidden" name="{{ redirect_field_name }}" value="{{ redirect_field_value }}">
                        {% endif %}
                    {% endslot %}
                    {% slot actions %}
                        <button type="submit" class="btn btn-warning w-100">Alterar Senha</button>
                    {% endslot %}
                {% endelement %}
                
                <div class="mt-3 text-center">
                    <a href="/">Voltar para home</a>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

### 6.6 account/password_reset.html (Recuperar Senha - Step 1)

```html
{% extends "base.html" %}
{% load allauth %}

{% block title %}Recuperar Senha{% endblock %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-md-6">
        <div class="card">
            <div class="card-header">
                <h3>Recuperar Senha</h3>
            </div>
            <div class="card-body">
                <p>Informe seu email para receber instruções de recuperação de senha.</p>
                
                {% element form method="post" action="/accounts/password/reset/" %}
                    {% csrf_token %}
                    {% slot body %}
                        {{ form.as_p }}
                        {% if redirect_field_value %}
                            <input type="hidden" name="{{ redirect_field_name }}" value="{{ redirect_field_value }}">
                        {% endif %}
                    {% endslot %}
                    {% slot actions %}
                        <button type="submit" class="btn btn-info w-100">Enviar Instruções</button>
                    {% endslot %}
                {% endelement %}
                
                <div class="mt-3 text-center">
                    <a href="{% url 'account_login' %}">Voltar para login</a>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

### 6.7 account/password_reset_done.html

```html
{% extends "base.html" %}

{% block title %}Email Enviado{% endblock %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-md-6 text-center">
        <div class="alert alert-success">
            <h4>Email Enviado!</h4>
            <p>Verifique sua caixa de email para instruções de como redefinir sua senha.</p>
            <p>O email pode demorar alguns minutos para chegar.</p>
            <a href="{% url 'account_login' %}" class="btn btn-primary">Voltar para Login</a>
        </div>
    </div>
</div>
{% endblock %}
```

### 6.8 account/password_reset_from_key.html (Nova Senha)

```html
{% extends "base.html" %}
{% load allauth %}

{% block title %}Nova Senha{% endblock %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-md-6">
        <div class="card">
            <div class="card-header">
                <h3>Digite Nova Senha</h3>
            </div>
            <div class="card-body">
                {% element form method="post" action="/accounts/password/reset/key/done/" %}
                    {% csrf_token %}
                    {% slot body %}
                        {{ form.as_p }}
                        {% if redirect_field_value %}
                            <input type="hidden" name="{{ redirect_field_name }}" value="{{ redirect_field_value }}">
                        {% endif %}
                    {% endslot %}
                    {% slot actions %}
                        <button type="submit" class="btn btn-success w-100">Salvar Nova Senha</button>
                    {% endslot %}
                {% endelement %}
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

### 6.9 account/password_reset_from_key_done.html

```html
{% extends "base.html" %}

{% block title %}Senha Alterada{% endblock %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-md-6 text-center">
        <div class="alert alert-success">
            <h4>Senha Alterada!</h4>
            <p>Sua senha foi redefinida com sucesso.</p>
            <a href="{% url 'account_login' %}" class="btn btn-primary">Ir para Login</a>
        </div>
    </div>
</div>
{% endblock %}
```

---

## 7. Configuração de Email (Para Recover Password)

Para que a funcionalidade de recuperação de senha funcione, você precisa configurar o envio de emails.

### 7.1 Configuração com Gmail

Adicione ao `settings.py`:

```python
# Email configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'seuemail@gmail.com'
EMAIL_HOST_PASSWORD = 'sua-senha-de-app'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
```

### 7.2 Como criar senha de app no Gmail

1. Acesse https://myaccount.google.com/security
2. Ative "Verificação em duas etapas"
3. Acesse https://myaccount.google.com/apppasswords
4. Selecione "Outro" e digite um nome (ex: "Django")
5. Copie a senha gerada e use no `EMAIL_HOST_PASSWORD`

### 7.3 Configuração de desenvolvimento (console)

Para testar sem enviar emails reais:

```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

Isso imprimirá os emails no terminal ao invés de enviá-los.

---

## 8. Executando o Projeto

### 8.1 Criar migrações

```bash
python manage.py makemigrations
python manage.py migrate
```

### 8.2 Criar superusuário (opcional)

```bash
python manage.py createsuperuser
```

### 8.3 Configurar Site no Admin

1. Execute o servidor: `python manage.py runserver`
2. Acesse `/admin` e faça login
3. Vá em **Sites** → **Sites**
4. Edite o site padrão:
   - **Domain name**: `localhost:8000`
   - **Display name**: `Meu Projeto`
5. Salve

### 8.4 Rodar servidor

```bash
python manage.py runserver
```

---

## 9. Fluxo de Uso

### 9.1 Login

1. Acesse `/accounts/login/`
2. Preencha email e senha
3. Clique em "Entrar"
4. Você será redirecionado para `/`

### 9.2 Criar Conta

1. Acesse `/accounts/signup/`
2. Preencha: username, email, senha e confirmação
3. Clique em "Cadastrar"
4. Você será redirecionado para `/` (já logado)

### 9.3 Alterar Senha (Logado)

1. Estando logado, clique em "Alterar Senha" no menu
2. Acesse `/accounts/password/change/`
3. Preencha: senha atual, nova senha, confirmação
4. Clique em "Alterar Senha"

### 9.4 Recuperar Senha

1. Acesse `/accounts/password/reset/`
2. Informe seu email cadastrado
3. Clique em "Enviar Instruções"
4. Verifique seu email (ou terminal se usando backend console)
5. Clique no link recebido
6. Você será redirecionado para página de nova senha
7. Digite a nova senha e confirme
8. Pronto! Use a nova senha para fazer login

---

## 10. Configurações Avançadas

### 10.1 Verificação de email obrigatória

Para exigir verificação de email após cadastro:

```python
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
```

Isso adiciona a etapa de confirmação por email antes do usuário poder fazer login.

### 10.2 Login apenas por email

Para usar apenas email (sem username):

```python
ACCOUNT_LOGIN_METHODS = {'email'}
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_SIGNUP_FIELDS = ['email*', 'password1*', 'password2*']
```

### 10.3 Login social

Consulte o tutorial específico: [django-allauth-social-login.md](./django-allauth-social-login.md)

---

## 11. Solução de Problemas

### 11.1 Templates não encontrados

Certifique-se de que:
- A pasta `templates/` foi criada no diretório raiz do projeto
- A configuração `DIRS` no `TEMPLATES` aponta para ela

### 11.2 Email não enviado

- Verifique as configurações de email no `settings.py`
- Confirme que o Site foi configurado no Admin
- Use `EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'` para debug

### 11.3 Redirect loops

Verifique se `LOGIN_REDIRECT_URL` e `LOGOUT_REDIRECT_URL` estão configurados corretamente.

---

## 12. Referências

- [Documentação oficial django-allauth](https://docs.allauth.org/)
- [Django Documentation](https://docs.djangoproject.com/)
- [Tutorial do projeto](https://github.com/pennersr/django-allauth)
