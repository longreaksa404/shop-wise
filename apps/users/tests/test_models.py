from django.test import TestCase
from apps.users.models import User


class UserModelTest(TestCase):

    def setUp(self):
        self.buyer = User.objects.create_user(
            email='buyer@test.com',
            username='testbuyer',
            password='testpass123',
            role=User.Role.BUYER
        )

    # test return format
    def test_user_str(self):
        self.assertEqual(str(self.buyer), 'testbuyer (buyer)')

    # test correct role
    def test_is_buyer(self):
        self.assertTrue(self.buyer.is_buyer)
        self.assertFalse(self.buyer.is_seller)
        self.assertFalse(self.buyer.is_admin)

    def test_is_seller(self):
        self.buyer.role = User.Role.SELLER
        self.assertTrue(self.buyer.is_seller)

    def test_is_admin(self):
        self.buyer.role = User.Role.ADMIN
        self.assertTrue(self.buyer.is_admin)

    # test login with email not username
    def test_email_is_login_field(self):
        self.assertEqual(User.USERNAME_FIELD, 'email')

    # test hash pw
    def test_password_is_hashed(self):
        self.assertFalse(self.buyer.password.startswith('testpass123'))