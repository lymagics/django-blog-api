import base64
from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APITestCase

from .models import Token
from .serializers import TokenSerializer

User = get_user_model()


class TokenModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='bob',
            email='bob@example.com',
            password='cat'
        )

        self.token = Token(user=self.user)
        self.token.generate()
        self.token.save()

    def test_token_generate(self):
        self.assertIsNotNone(self.token.access_token)
        self.assertIsNotNone(self.token.refresh_token)
        self.assertGreater(self.token.access_expiration, datetime.utcnow())
        self.assertGreater(self.token.refresh_expiration, datetime.utcnow())

    def test_token_expire(self):
        self.token.expire()

        self.assertLess(self.token.access_expiration, datetime.utcnow())
        self.assertLess(self.token.refresh_expiration, datetime.utcnow())

    def test_clean(self):
        before_yesterday = datetime.utcnow() - timedelta(days=2)
        self.token.access_expiration = before_yesterday
        self.token.refresh_expiration = before_yesterday
        self.token.save()

        Token.clean()
        
        self.assertEqual(Token.objects.count(), 0)


class TokenSerializerTests(TestCase):
    def test_valid_data(self):
        data = {
            'access_token': 'djweqjcsjkqdjiwgfuiajkfqLfq'
        } 

        serializer = TokenSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_data(self):
        data = {
            'access_token': None
        } 

        serializer = TokenSerializer(data=data)
        self.assertFalse(serializer.is_valid())


class TokenAPITests(APITestCase):
    @classmethod 
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='bob',
            email='bob@example.com',
            password='dog'
        ) 

    def provide_basic_auth(self):
        credentials = base64.b64encode(b'bob:dog').decode('ascii')
        self.client.credentials(HTTP_AUTHORIZATION=f'Basic {credentials}')

    def provide_token_auth(self, token):
        self.client.credentials(HTTP_AUTHORIZATiON=f'Bearer {token}')

    def test_create_token(self):
        self.provide_basic_auth()

        resp = self.client.post('/tokens/')
        self.assertEqual(resp.status_code, 201)
        self.assertTrue('access_token' in resp.data) 

    def test_refresh_token(self):
        self.provide_basic_auth()

        resp = self.client.post('/tokens/')
        self.assertEqual(resp.status_code, 201)

        token = resp.data['refresh_token'] if settings.REFRESH_TOKEN_IN_BODY else resp.cookies['refresh_token']

        data = {
            'refresh_token': token
        }
        resp = self.client.put('/tokens/', data)
        self.assertEqual(resp.status_code, 201)
       
    def test_revoke_token(self):
        self.provide_basic_auth()

        resp = self.client.post('/tokens/')
        self.assertEqual(resp.status_code, 201)

        access_token = resp.data['access_token']
        refresh_token = resp.data['refresh_token'] if settings.REFRESH_TOKEN_IN_BODY else resp.cookies['refresh_token']

        data = {
            'refresh_token': refresh_token
        }
        resp = self.client.delete('/tokens/', data=data)
        self.assertEqual(resp.status_code, 204)

        self.provide_token_auth(access_token)
        resp = self.client.get('/users/me/')
        self.assertEqual(resp.status_code, 403)
