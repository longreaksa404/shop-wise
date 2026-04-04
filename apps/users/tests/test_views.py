from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from apps.users.models import User


class RegisterViewTest(APITestCase):

    def test_cannot_register_as_admin(self):
        data = {
            'username': 'hacker',
            'email': 'hacker@test.com',
            'password': 'testpass123',
            'password2': 'testpass123',
            'role': 'admin'
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    # validate data and status return
    def test_register_success(self):
        data = {
            'username': 'newuser',
            'email': 'new@test.com',
            'password': 'testpass123',
            'password2': 'testpass123',
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'success')


    def test_register_duplicate_email(self):
        User.objects.create_user(
            email='dupe@test.com',
            username='existing',
            password='testpass123'
        )
        data = {
            'username': 'newuser',
            'email': 'dupe@test.com',
            'password': 'testpass123',
            'password2': 'testpass123',
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_password_mismatch(self):
        data = {
            'username': 'newuser',
            'email': 'new@test.com',
            'password': 'testpass123',
            'password2': 'wrongpass123',
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # fail if missing field
    def test_register_missing_fields(self):
        response = self.client.post(reverse('register'), {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginViewTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email='login@test.com',
            username='loginuser',
            password='testpass123'
        )

    def test_login_success(self):
        data = {'email': 'login@test.com', 'password': 'testpass123'}
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'success')
        self.assertIn('access', response.data['token'])
        self.assertIn('refresh', response.data['token'])

    def test_login_wrong_password(self):
        data = {'email': 'login@test.com', 'password': 'wrongpass'}
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_wrong_email(self):
        data = {'email': 'wrong@test.com', 'password': 'testpass123'}
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # cant login if user dont active
    def test_login_inactive_user(self):
        self.user.is_active = False
        self.user.save()
        data = {'email': 'login@test.com', 'password': 'testpass123'}
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ProfileViewTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email='profile@test.com',
            username='profileuser',
            password='testpass123'
        )
        response = self.client.post(reverse('login'), {
            'email': 'profile@test.com',
            'password': 'testpass123'
        })
        self.token = response.data['token']['access']

    # token required to see profile
    def test_get_profile_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'profile@test.com')

    # cant view otheer profile if unauthenticated
    def test_get_profile_unauthenticated(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # cann update username
    def test_update_profile_username(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.put(reverse('profile'), {'username': 'updatedname'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user']['username'], 'updatedname')

    # email is read only
    def test_cannot_update_email(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.put(reverse('profile'), {'email': 'hacked@test.com'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user']['email'], 'profile@test.com')

    # role is read only
    def test_cannot_update_role(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.put(reverse('profile'), {'role': 'admin'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user']['role'], 'buyer')