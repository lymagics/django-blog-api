from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APITestCase

from tokens.models import Token
from .serializers import UserSerializer

User = get_user_model()


class UserModelTests(TestCase):
    @classmethod 
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='bob',
            email='bob@example.com',
            password='dog'
        )

        cls.super_user = User.objects.create_superuser(
            username='alice',
            email='alice@example.com',
            password='cat'
        )

    def test_regular_user(self):
        self.assertEqual(self.user.username, 'bob')
        self.assertEqual(self.user.email, 'bob@example.com')
        self.assertEqual(str(self.user), 'bob')
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)

    def test_super_user(self):
        self.assertEqual(self.super_user.username, 'alice')
        self.assertEqual(self.super_user.email, 'alice@example.com')
        self.assertEqual(str(self.super_user), 'alice')
        self.assertTrue(self.super_user.is_staff)
        self.assertTrue(self.super_user.is_superuser)


class UserSerializerTests(TestCase):
    def test_valid_data(self):
        data = {
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'dog'
        }

        serializer = UserSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_data(self):
        data = {
            'email': 'sure_invaild_email'
        }

        serializer = UserSerializer(data=data)
        self.assertFalse(serializer.is_valid())


class UserAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='bob',
            email='bob@example.com',
            password='dog'
        ) 

    def provide_token(self):
        token = Token(user=self.user)
        token.generate()
        token.save()

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token.access_token}')

    def test_retrieve_all_users(self):
        resp = self.client.get('/users/')

        self.assertEqual(resp.status_code, 200)
        self.assertTrue('limit' in resp.data)
        self.assertTrue('offset' in resp.data)
        self.assertEqual(len(resp.data['data']), 1)

    def test_create_new_user(self):
        data = {
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'cat'
        }

        resp = self.client.post('/users/', data)

        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.data['username'], 'alice')
        self.assertTrue('email' not in resp.data)
        self.assertTrue('last_seen' in resp.data)
        self.assertTrue('member_since' in resp.data)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(User.objects.last().username, 'alice')

    def test_retrieve_user_by_username(self):
        resp = self.client.get('/users/bob/')

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['username'], 'bob')
        self.assertTrue('email' not in resp.data)
        self.assertTrue('password' not in resp.data)

    def test_retrieve_authenticated_user(self):
        self.provide_token()

        resp = self.client.get('/users/me/')

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['username'], 'bob')
        self.assertTrue('email' not in resp.data)

    def test_update_authenticated_user(self):
        self.provide_token()

        data = {
            'username': 'alice',
            'email': 'alice@example.com'
        }

        resp = self.client.put('/users/me/', data)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['username'], 'alice')
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, 'alice@example.com')
