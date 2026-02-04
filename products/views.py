from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import models
from django.contrib.auth.models import User
from .models import Product, Category, PriceHistory
from .forms import ProductForm, CategoryForm
from django.contrib import messages


# --- Product Views ---
@login_required
def product_list(request):
    if "clear" in request.GET:
        if "filters_dashboard" in request.session:
            del request.session["filters_dashboard"]
        return redirect("product_list")

    session_filters = request.session.get("filters_dashboard", {})

    q = request.GET.get("q") if "q" in request.GET else session_filters.get("q", "")
    status = (
        request.GET.get("status")
        if "status" in request.GET
        else session_filters.get("status", "")
    )
    min_price = (
        request.GET.get("min_price")
        if "min_price" in request.GET
        else session_filters.get("min_price", "")
    )
    max_price = (
        request.GET.get("max_price")
        if "max_price" in request.GET
        else session_filters.get("max_price", "")
    )
    min_stock = (
        request.GET.get("min_stock")
        if "min_stock" in request.GET
        else session_filters.get("min_stock", "")
    )
    max_stock = (
        request.GET.get("max_stock")
        if "max_stock" in request.GET
        else session_filters.get("max_stock", "")
    )
    category_id = (
        request.GET.get("category")
        if "category" in request.GET
        else session_filters.get("category", "")
    )

    request.session["filters_dashboard"] = {
        "q": q,
        "status": status,
        "category": category_id,
        "min_price": min_price,
        "max_price": max_price,
        "min_stock": min_stock,
        "max_stock": max_stock,
    }

    products = Product.objects.filter(user=request.user)

    if q:
        products = products.filter(name__icontains=q) | products.filter(
            description__icontains=q
        )
    if category_id:
        products = products.filter(categories=category_id)

    if status == "public":
        products = products.filter(is_public=True)
    elif status == "private":
        products = products.filter(is_public=False)
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    if min_stock:
        products = products.filter(stock__gte=min_stock)
    if max_stock:
        products = products.filter(stock__lte=max_stock)

    products = products.distinct().order_by("-created_at")

    stats = {
        "total_count": products.count(),
        "total_stock": sum(p.stock for p in products),
        "total_value": sum(p.price * p.stock for p in products),
    }

    return render(
        request,
        "products/product_list.html",
        {
            "products": products,
            "categories": Category.objects.all(),
            "stats": stats,
            "q": q,
            "status": status,
            "category_id": category_id,
            "min_price": min_price,
            "max_price": max_price,
            "min_stock": min_stock,
            "max_stock": max_stock,
        },
    )


@login_required
def product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()
            form.save_m2m()  # Important for ManyToMany fields
            messages.success(request, f'Produto "{product.name}" criado com sucesso!')
            return redirect("product_list")
    else:
        form = ProductForm()
    return render(
        request, "products/product_form.html", {"form": form, "title": "Add Product"}
    )


@login_required
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk, user=request.user)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(
                request, f'Produto "{product.name}" atualizado com sucesso!'
            )
            return redirect("product_list")
    else:
        form = ProductForm(instance=product)
    return render(
        request,
        "products/product_form.html",
        {"form": form, "title": "Edit Product", "product": product},
    )


@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk, user=request.user)
    if request.method == "POST":
        product_name = product.name
        product.delete()
        messages.success(request, f'Produto "{product_name}" removido permanentemente.')
        return redirect("product_list")
    return render(request, "products/product_confirm_delete.html", {"product": product})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)

    # Se o produto for privado, apenas o dono pode ver (exige estar logado e ser o dono)
    if not product.is_public:
        if not request.user.is_authenticated or product.user != request.user:
            messages.error(request, "Você não tem permissão para ver este produto.")
            return redirect("account_login")

    return render(request, "products/product_detail_modal.html", {"product": product})


def price_history_view(request, pk):
    product = get_object_or_404(Product, pk=pk)

    # Verificação de permissão
    if not product.is_public:
        if not request.user.is_authenticated or product.user != request.user:
            messages.error(request, "Você não tem permissão para ver este produto.")
            return redirect("account_login")

    # Filtros de data
    price_history = product.price_history.all()

    data_inicio = request.GET.get("data_inicio")
    data_fim = request.GET.get("data_fim")

    if data_inicio:
        try:
            from datetime import datetime

            data_inicio_obj = datetime.strptime(data_inicio, "%Y-%m-%d")
            price_history = price_history.filter(changed_at__gte=data_inicio_obj)
        except ValueError:
            pass

    if data_fim:
        try:
            from datetime import datetime, timedelta

            data_fim_obj = datetime.strptime(data_fim, "%Y-%m-%d")
            # Adiciona 1 dia para incluir todo o dia final
            data_fim_obj = data_fim_obj + timedelta(days=1)
            price_history = price_history.filter(changed_at__lt=data_fim_obj)
        except ValueError:
            pass

    return render(
        request,
        "products/price_history.html",
        {
            "product": product,
            "price_history": price_history,
            "data_inicio": data_inicio,
            "data_fim": data_fim,
        },
    )


def price_history_overview(request):
    """Dashboard consolidado de histórico de preços de todos os produtos"""
    from django.db.models import Count
    from datetime import datetime, timedelta

    # Apenas produtos do usuário logado
    if not request.user.is_authenticated:
        messages.error(request, "Você precisa estar logado para acessar esta página.")
        return redirect("account_login")

    # Base Queryset com otimização de prefetch
    user_products = Product.objects.filter(user=request.user).prefetch_related(
        "price_history"
    )

    # Filtro por Termo de Busca (q)
    q = request.GET.get("q", "")
    if q:
        user_products = user_products.filter(
            models.Q(name__icontains=q) | models.Q(description__icontains=q)
        )

    # Filtro por Categoria
    category_id = request.GET.get("category")
    if category_id:
        user_products = user_products.filter(categories__id=category_id)

    # Estatísticas gerais
    total_alteracoes = PriceHistory.objects.filter(product__in=user_products).count()

    # Produto com mais alterações
    produto_mais_alteracoes_obj = (
        user_products.annotate(num_alteracoes=Count("price_history"))
        .order_by("-num_alteracoes")
        .first()
    )
    produto_mais_alteracoes = {
        "produto": produto_mais_alteracoes_obj,
        "count": (
            produto_mais_alteracoes_obj.num_alteracoes
            if produto_mais_alteracoes_obj
            else 0
        ),
    }

    # Calcular maior aumento e redução percentual
    maior_aumento = {"produto": None, "percentual": 0}
    maior_reducao = {"produto": None, "percentual": 0}

    # Query otimizada para buscar os dois últimos preços de todos os produtos
    from django.db.models import OuterRef, Subquery

    latest_prices = PriceHistory.objects.filter(product=OuterRef("pk")).order_by(
        "-changed_at"
    )
    products_with_prices = user_products.annotate(
        current_price=Subquery(latest_prices.values("price")[:1]),
        previous_price=Subquery(latest_prices.values("price")[1:2]),
    ).filter(previous_price__isnull=False)

    for p in products_with_prices:
        if p.current_price > p.previous_price:
            percentual = ((p.current_price - p.previous_price) / p.previous_price) * 100
            if percentual > maior_aumento["percentual"]:
                maior_aumento["percentual"] = percentual
                maior_aumento["produto"] = p
        elif p.current_price < p.previous_price:
            percentual = ((p.previous_price - p.current_price) / p.previous_price) * 100
            if percentual > maior_reducao["percentual"]:
                maior_reducao["percentual"] = percentual
                maior_reducao["produto"] = p

    # Média de alterações por produto
    total_produtos = user_products.count()
    media_alteracoes = total_alteracoes / total_produtos if total_produtos > 0 else 0

    # Produtos com seus históricos (para lista principal)
    produtos_com_historico = []
    for product in user_products:
        # Ordenação em Python para aproveitar o prefetch_related e evitar N+1 queries
        history = sorted(
            product.price_history.all(), key=lambda x: x.changed_at, reverse=True
        )

        if not history:
            continue

        # Dados para o Sparkline (últimos 10 preços, ordem cronológica)
        history_prices = [float(h.price) for h in history[:10]]
        history_prices.reverse()  # Reverte para o gráfico (do mais antigo para o mais novo)

        # Determinar tendência
        latest = history[0]
        previous = history[1] if len(history) > 1 else None
        trend = "stable"

        if previous:
            if latest.price > previous.price:
                trend = "up"
            elif latest.price < previous.price:
                trend = "down"

        produtos_com_historico.append(
            {
                "produto": product,
                "historico_precos": history_prices,
                "total_alteracoes": len(history),
                "ultima_alteracao": latest,
                "trend": trend,
            }
        )

    # Ordenar por data da última alteração
    produtos_com_historico.sort(
        key=lambda x: (
            x["ultima_alteracao"].changed_at if x["ultima_alteracao"] else datetime.min
        ),
        reverse=True,
    )

    context = {
        "total_alteracoes": total_alteracoes,
        "produto_mais_alteracoes": produto_mais_alteracoes,
        "maior_aumento": maior_aumento,
        "maior_reducao": maior_reducao,
        "media_alteracoes": media_alteracoes,
        "produtos_com_historico": produtos_com_historico,
        "categorias": Category.objects.filter(products__user=request.user).distinct(),
        "selected_category": int(category_id) if category_id else "",
        "q": q,
    }

    return render(request, "products/price_history_overview.html", context)


# --- Category Views ---
@login_required
def category_list(request):
    if "clear" in request.GET:
        if "filters_categories" in request.session:
            del request.session["filters_categories"]
        return redirect("category_list")

    session_filters = request.session.get("filters_categories", {})
    q = request.GET.get("q") if "q" in request.GET else session_filters.get("q", "")

    request.session["filters_categories"] = {"q": q}

    categories = Category.objects.all()
    if q:
        categories = categories.filter(
            models.Q(name__icontains=q)
            | models.Q(description__icontains=q)
            | models.Q(slug__icontains=q)
        )

    categories = categories.order_by("name")
    return render(
        request, "products/category_list.html", {"categories": categories, "q": q}
    )


@login_required
def category_create(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Categoria criada com sucesso!")
            return redirect("category_list")
    else:
        form = CategoryForm()
    return render(
        request,
        "products/category_form.html",
        {"form": form, "title": "Nova Categoria"},
    )


@login_required
def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Categoria atualizada com sucesso!")
            return redirect("category_list")
    else:
        form = CategoryForm(instance=category)
    return render(
        request,
        "products/category_form.html",
        {"form": form, "title": "Editar Categoria", "category": category},
    )


@login_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        category.delete()
        messages.success(request, "Categoria removida com sucesso.")
        return redirect("category_list")
    return render(
        request, "products/category_confirm_delete.html", {"category": category}
    )


@login_required
def category_duplicate(request, pk):
    original_category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Categoria duplicada com sucesso!")
            return redirect("category_list")
    else:
        # Preenche os dados iniciais, mas limpa o slug para forçar um novo ou alteração
        initial_data = {
            "name": f"{original_category.name} (Cópia)",
            "description": original_category.description,
            "color": original_category.color,
            "slug": f"{original_category.slug}-copia",
        }
        form = CategoryForm(initial=initial_data)

    return render(
        request,
        "products/category_form.html",
        {"form": form, "title": "Duplicar Categoria", "is_duplicate": True},
    )


# --- Account & System Views ---
@login_required
def profile_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        user = request.user
        user.username = username
        user.email = email
        user.save()
        messages.success(request, "Perfil atualizado com sucesso!")
        return redirect("profile")
    return render(request, "account/profile.html")


@login_required
def delete_account_view(request):
    if request.method == "POST":
        password = request.POST.get("password")
        user = request.user

        # Verify password
        from django.contrib.auth import authenticate

        authenticated_user = authenticate(username=user.username, password=password)

        if authenticated_user is not None:
            user.delete()
            messages.success(request, "Sua conta foi excluída permanentemente.")
            return redirect("account_login")
        else:
            messages.error(
                request, "Falha na exclusão: A senha informada está incorreta."
            )
            return redirect("profile")

    return redirect("profile")


def user_public_catalog(request, username):
    catalog_user = get_object_or_404(User, username=username)
    products = Product.objects.filter(user=catalog_user, is_public=True)

    q = request.GET.get("q")
    if q:
        products = products.filter(name__icontains=q) | products.filter(
            description__icontains=q
        )

    category_id = request.GET.get("category")
    if category_id:
        products = products.filter(categories=category_id)

    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    min_stock = request.GET.get("min_stock")
    max_stock = request.GET.get("max_stock")
    if min_stock:
        products = products.filter(stock__gte=min_stock)
    if max_stock:
        products = products.filter(stock__lte=max_stock)

    products = products.distinct().order_by("-created_at")

    stats = {
        "total_count": products.count(),
        "total_stock": sum(p.stock for p in products),
        "total_value": sum(p.price * p.stock for p in products),
    }

    return render(
        request,
        "products/product_list.html",
        {
            "products": products,
            "categories": Category.objects.all(),
            "stats": stats,
            "title": f"Catálogo de {catalog_user.username}",
            "is_public_view": True,
            "q": q,
            "category_id": request.GET.get("category", ""),
            "min_price": min_price,
            "max_price": max_price,
            "min_stock": min_stock,
            "max_stock": max_stock,
        },
    )


def public_product_list(request):
    products = Product.objects.filter(is_public=True)
    q = request.GET.get("q")
    if q:
        products = products.filter(name__icontains=q) | products.filter(
            description__icontains=q
        )

    category_id = request.GET.get("category")
    if category_id:
        products = products.filter(categories=category_id)

    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    min_stock = request.GET.get("min_stock")
    max_stock = request.GET.get("max_stock")
    if min_stock:
        products = products.filter(stock__gte=min_stock)
    if max_stock:
        products = products.filter(stock__lte=max_stock)

    products = products.distinct().order_by("-created_at")

    stats = {
        "total_count": products.count(),
        "total_stock": sum(p.stock for p in products),
        "total_value": sum(p.price * p.stock for p in products),
    }

    return render(
        request,
        "products/product_list.html",
        {
            "products": products,
            "categories": Category.objects.all(),
            "stats": stats,
            "title": "Catálogo Público",
            "is_public_view": True,
            "q": q,
            "category_id": request.GET.get("category", ""),
            "min_price": min_price,
            "max_price": max_price,
            "min_stock": min_stock,
            "max_stock": max_stock,
        },
    )


def toggle_theme(request):
    current_theme = request.session.get("theme", "light")
    new_theme = "dark" if current_theme == "light" else "light"
    request.session["theme"] = new_theme
    if request.user.is_authenticated:
        profile = request.user.profile
        profile.theme = new_theme
        profile.save()
    return redirect(request.META.get("HTTP_REFERER", "/"))


from django.contrib.auth import logout


@login_required
def logout_view(request):
    if request.method == "POST":
        theme = request.session.get("theme", "light")
        logout(request)
        request.session["theme"] = theme
        messages.success(request, "Você saiu do sistema.")
        return redirect("account_login")
    return redirect("product_list")


def set_view_mode(request, mode):
    if mode in ["grid", "table"]:
        request.session["view_mode"] = mode
    return redirect(request.META.get("HTTP_REFERER", "/"))
