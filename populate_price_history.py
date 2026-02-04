"""
Script para popular o histórico de preços de produtos existentes.
Execute com: python manage.py shell < populate_price_history.py
"""

from products.models import Product, PriceHistory

# Para cada produto que não tem histórico, cria o registro inicial
for product in Product.objects.all():
    if not product.price_history.exists():
        PriceHistory.objects.create(product=product, price=product.price)
        print(f"✓ Histórico criado para: {product.name} - R$ {product.price}")
    else:
        print(f"- {product.name} já possui histórico")

print("\n✅ Migração de histórico de preços concluída!")
