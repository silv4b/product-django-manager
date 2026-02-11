import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from products.models import Product, Category, ProductMovement


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    return User.objects.create_user(
        username="testuser", password="password123", email="test@example.html"
    )


@pytest.fixture
def other_user(db):
    return User.objects.create_user(
        username="otheruser", password="password123", email="other@example.html"
    )


@pytest.fixture
def auth_client(api_client, user):
    response = api_client.post(
        reverse("token_obtain_pair"),
        {"username": "testuser", "password": "password123"},
    )
    token = response.data["access"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return api_client


@pytest.fixture
def category(user):
    return Category.objects.create(user=user, name="Hardware", slug="hardware")


@pytest.fixture
def product(user, category):
    p = Product.objects.create(user=user, name="Teclado", price=150.00, stock=10)
    p.categories.add(category)
    return p


@pytest.mark.django_db
class TestAuthentication:
    def test_obtain_token(self, api_client, user):
        url = reverse("token_obtain_pair")
        response = api_client.post(
            url, {"username": "testuser", "password": "password123"}
        )
        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data
        assert "refresh" in response.data


@pytest.mark.django_db
class TestCategoryAPI:
    def test_list_categories(self, auth_client, category):
        url = reverse("category-list")
        response = auth_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        # 4 default categories + 1 Hardware
        assert len(response.data) == 5
        assert any(c["name"] == "Hardware" for c in response.data)

    def test_create_category(self, auth_client):
        url = reverse("category-list")
        data = {"name": "Nova Categoria", "slug": "nova-categoria", "color": "#ff0000"}
        response = auth_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Category.objects.filter(name="Nova Categoria").exists()


@pytest.mark.django_db
class TestProductAPI:
    def test_list_products(self, auth_client, product):
        url = reverse("product-list")
        response = auth_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["name"] == "Teclado"

    def test_create_product(self, auth_client, category):
        url = reverse("product-list")
        data = {
            "name": "Mouse Gamer",
            "price": "89.90",
            "stock": 5,
            "category_ids": [category.id],
        }
        response = auth_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Product.objects.filter(name="Mouse Gamer").exists()

    def test_product_detail(self, auth_client, product):
        url = reverse("product-detail", args=[product.id])
        response = auth_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert "price_history" in response.data
        assert "movements" in response.data

    def test_other_user_cannot_access_product(self, api_client, other_user, product):
        # Authenticate as other_user
        response = api_client.post(
            reverse("token_obtain_pair"),
            {"username": "otheruser", "password": "password123"},
        )
        token = response.data["access"]
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        url = reverse("product-detail", args=[product.id])
        response = api_client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestMovementAPI:
    def test_perform_in_movement(self, auth_client, product):
        url = reverse("product-movement", args=[product.id])
        data = {"type": "IN", "quantity": 5, "reason": "Compra"}
        response = auth_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED

        product.refresh_from_db()
        assert product.stock == 15  # 10 initial + 5

    def test_perform_out_movement_insufficient_stock(self, auth_client, product):
        url = reverse("product-movement", args=[product.id])
        data = {"type": "OUT", "quantity": 50, "reason": "Venda Grande"}
        response = auth_client.post(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "insuficiente" in response.data["error"]
