from django.test import TestCase
from apps.users.models import User
from apps.products.models import Category, Product


class CategoryModelTest(TestCase):

    # correct name format
    def test_category_str(self):
        cat = Category.objects.create(name='Electronics')
        self.assertEqual(str(cat), 'Electronics')

    # show parent and chile category correctly
    def test_subcategory_str(self):
        parent = Category.objects.create(name='Electronics')
        child = Category.objects.create(name='Phones', parent_category=parent)
        self.assertEqual(str(child), 'Electronics - Phones')

    # can create without parent
    def test_parent_category_is_optional(self):
        cat = Category.objects.create(name='Books')
        self.assertIsNone(cat.parent_category)


class ProductModelTest(TestCase):

    def setUp(self):
        self.seller = User.objects.create_user(
            email='seller@test.com',
            username='testseller',
            password='testpass123',
            role=User.Role.SELLER
        )
        self.product = Product.objects.create(
            name='iPhone',
            price=999.99,
            stock_quantity=10,
            seller=self.seller
        )

    # display correct name and price
    def test_product_str(self):
        self.assertEqual(str(self.product), 'iPhone ($999.99)')

    def test_is_in_stock_true(self):
        self.assertTrue(self.product.is_in_stock)

    def test_is_in_stock_false(self):
        self.product.stock_quantity = 0
        self.assertFalse(self.product.is_in_stock)

    # prodcut can exist without category
    def test_category_is_optional(self):
        self.assertIsNone(self.product.category)