# Tutorial: Adicionando Basecoat UI a um Projeto Django

Este tutorial explica como o Basecoat UI foi adicionado ao projeto Kore Product Manager, permitindo que você replique em futuros projetos.

## O que é o Basecoat UI?

Basecoat UI é um framework CSS moderno baseado em Tailwind CSS que oferece componentes prontos e um design system consistente.

## Pré-requisitos

- Node.js instalado
- Projeto Django existente

---

## Passo 1: Inicializar o npm

No diretório raiz do seu projeto Django, inicialize o npm:

```bash
npm init -y
```

## Passo 2: Instalar as dependências

Instale o Tailwind CSS e o Basecoat UI:

```bash
npm install -D tailwindcss @tailwindcss/cli postcss autoprefixer postcss-import
npm install basecoat-css
```

## Passo 3: Criar a estrutura de arquivos CSS

Crie o arquivo `static/css/input.css`:

```css
@import "tailwindcss";
@import "../../node_modules/basecoat-css/dist/basecoat.css";

@source "../../templates/**/*.html";
@source "../../products/**/*.py";

@theme {
    --font-sans: "Inter", ui-sans-serif, system-ui, sans-serif;
}

html,
body {
    font-family: var(--font-sans);
}
```

## Passo 4: Configurar scripts npm

No `package.json`, adicione os scripts:

```json
"scripts": {
    "watch": "tailwindcss -i ./static/css/input.css -o ./static/css/output.css --watch",
    "build": "tailwindcss -i ./static/css/input.css -o ./static/css/output.css --minify"
}
```

## Passo 5: Compilar o CSS

Execute o comando para gerar o CSS final:

```bash
npm run build
```

Para desenvolvimento com watch mode:

```bash
npm run watch
```

## Passo 6: Configurar o template base

No `templates/base.html`, adicione o CSS compilado:

```html
{% load static %}
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Seu Projeto</title>
    <link href="{% static 'css/output.css' %}" rel="stylesheet">
    <!-- Ícones (opcional) -->
    <script src="https://unpkg.com/lucide@latest"></script>
    <!-- HTMX (opcional) -->
    <script src="https://unpkg.com/htmx.org@1.9.10"></script>
</head>
<body class="bg-background text-foreground antialiased min-h-screen flex flex-col">
    <header>
        <!-- Seu header aqui -->
    </header>
    
    <main class="flex-1 container mx-auto px-4 py-8">
        {% block content %}
        {% endblock %}
    </main>
    
    <script src="{% static 'js/main.js' %}"></script>
</body>
</html>
```

## Passo 7: Usar componentes Basecoat UI

Agora você pode usar as classes do Basecoat UI. Exemplos:

### Botões
```html
<button class="btn btn-primary">Primary</button>
<button class="btn btn-secondary">Secondary</button>
<button class="btn btn-ghost">Ghost</button>
<button class="btn btn-destructive">Danger</button>
<button class="btn btn-sm">Small</button>
<button class="btn btn-lg">Large</button>
```

### Cards
```html
<div class="card">
    <header>
        <h2 class="text-xl font-bold">Título</h2>
    </header>
    <section>
        Conteúdo do card
    </section>
    <footer>
        <button class="btn btn-primary">Ação</button>
    </footer>
</div>
```

### Formulários
```html
<form>
    <label class="field">
        <span class="field-label">Nome</span>
        <input type="text" class="field-input" placeholder="Seu nome">
    </label>
    <button type="submit" class="btn btn-primary mt-4">Enviar</button>
</form>
```

### Toasts
```html
<div class="toaster">
    <div class="toast">
        <div class="toast-content">
            <i data-lucide="check-circle"></i>
            <section>
                <h2>Sucesso</h2>
                <p>Mensagem de sucesso</p>
            </section>
            <footer>
                <button class="btn btn-sm" data-toast-cancel>Fechar</button>
            </footer>
        </div>
    </div>
</div>
```

### Tabelas
```html
<table class="table">
    <thead>
        <tr>
            <th>Coluna 1</th>
            <th>Coluna 2</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Dado 1</td>
            <td>Dado 2</td>
        </tr>
    </tbody>
</table>
```

### Badges
```html
<span class="badge">Badge</span>
<span class="badge badge-primary">Primary</span>
<span class="badge badge-secondary">Secondary</span>
<span class="badge badge-outline">Outline</span>
```

### Modais
```html
<div class="card max-w-sm w-full">
    <header>
        <h2 class="text-xl font-bold">Título do Modal</h2>
    </header>
    <section>
        Conteúdo
    </section>
    <footer>
        <button class="btn">Cancelar</button>
        <button class="btn btn-primary">Confirmar</button>
    </footer>
</div>
```

## Passo 8: Adicionar arquivos JavaScript

Crie `static/js/main.js` para inicializar ícones e funcionalidades:

```javascript
// Inicializar ícones Lucide
if (typeof lucide !== 'undefined') {
    lucide.createIcons();
}

// Funções utilitárias
function closeToast(button) {
    const toast = button.closest('.toast');
    if (toast) {
        toast.remove();
    }
}

function toggleLogoutModal(show) {
    const modal = document.getElementById('logoutModal');
    if (modal) {
        modal.classList.toggle('hidden', !show);
        modal.classList.toggle('flex', show);
    }
}
```

## Configurações Opcionais

### Theme escuro (dark mode)

No `templates/base.html`, adicione a classe `dark` ao elemento `<html>`:

```html
<html class="dark">
```

O Basecoat UI suporta dark mode automaticamente com as classes `dark:bg-*`, `dark:text-*`, etc.

### Adicionar ao .gitignore

Exclude `node_modules` e o CSS compilado do repositório:

```gitignore
node_modules/
static/css/output.css
```

### Collectstatic no Django

Ao fazer deploy, não se esqueça de executar:

```bash
python manage.py collectstatic
```

---

## Referências

- [Documentação Basecoat UI](https://basecoatui.com/)
- [Tailwind CSS v4](https://tailwindcss.com/)
- [Lucide Icons](https://lucide.dev/)
