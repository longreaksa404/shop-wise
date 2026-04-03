from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from apps.users.models import User
from apps.products.models import Category, Product


class CategoryViewTest(APITestCase):

    def setUp(self):
        self.admin = User.objects.create_user(
            email='admin@test.com',
            username='testadmin',
            password='testpass123',
            role=User.Role.ADMIN
        )
        self.buyer = User.objects.create_user(
            email='buyer@test.com',
            username='testbuyer',
            password='testpass123',
            role=User.Role.BUYER
        )
        self.category = Category.objects.create(name='Electronics')

    def _get_token(self, email, password):
        response = self.client.post(reverse('login'), {
            'email': email,
            'password': password
        })
        return response.data['token']['access']

    def test_list_categories_public(self):
        response = self.client.get(reverse('category-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'success')

    def test_admin_can_create_category(self):
        token = self._get_token('admin@test.com', 'testpass123')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.post(reverse('category-list'), {'name': 'Clothing'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_buyer_cannot_create_category(self):
        token = self._get_token('buyer@test.com', 'testpass123')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.post(reverse('category-list'), {'name': 'Clothing'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_cannot_create_category(self):
        response = self.client.post(reverse('category-list'), {'name': 'Clothing'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ProductViewTest(APITestCase):

    def setUp(self):
        self.seller = User.objects.create_user(
            email='seller@test.com',
            username='testseller',
            password='testpass123',
            role=User.Role.SELLER
        )
        self.seller2 = User.objects.create_user(
            email='seller2@test.com',
            username='testseller2',
            password='testpass123',
            role=User.Role.SELLER
        )
        self.buyer = User.objects.create_user(
            email='buyer@test.com',
            username='testbuyer',
            password='testpass123',
            role=User.Role.BUYER
        )
        self.product = Product.objects.create(
            name='iPhone',
            price=999.99,
            stock_quantity=10,
            seller=self.seller
        )

    def _get_token(self, email, password):
        response = self.client.post(reverse('login'), {
            'email': email,
            'password': password
        })
        return response.data['token']['access']

    def test_list_products_public(self):
        response = self.client.get(reverse('product-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_product_detail_public(self):
        response = self.client.get(reverse('product-detail', args=[self.product.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['name'], 'iPhone')

    def test_seller_can_create_product(self):
        token = self._get_token('seller@test.com', 'testpass123')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        data = {'name': 'Samsung Galaxy', 'price': '799.99', 'stock_quantity': 5}
        response = self.client.post(reverse('product-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_buyer_cannot_create_product(self):
        token = self._get_token('buyer@test.com', 'testpass123')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        data = {'name': 'Samsung Galaxy', 'price': '799.99', 'stock_quantity': 5}
        response = self.client.post(reverse('product-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_seller_can_update_own_product(self):
        token = self._get_token('seller@test.com', 'testpass123')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.put(
            reverse('product-detail', args=[self.product.pk]),
            {'name': 'iPhone Updated', 'price': '899.99', 'stock_quantity': 8}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_seller_cannot_update_other_sellers_product(self):
        token = self._get_token('seller2@test.com', 'testpass123')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.put(
            reverse('product-detail', args=[self.product.pk]),
            {'name': 'Hacked', 'price': '1.00', 'stock_quantity': 0}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_seller_can_delete_own_product(self):
        token = self._get_token('seller@test.com', 'testpass123')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.delete(
            reverse('product-detail', args=[self.product.pk])
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_price_rejected(self):
        token = self._get_token('seller@test.com', 'testpass123')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        data = {'name': 'Bad Product', 'price': '-10.00', 'stock_quantity': 5}
        response = self.client.post(reverse('product-list'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)