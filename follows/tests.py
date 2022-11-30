import base64

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APITestCase

User = get_user_model()


class FollowSystemTests(TestCase):
    def setUp(self):
        self.u1 = User.objects.create_user(
            username='bob',
            email='bob@example.com',
            password='dog'
        ) 

        self.u2 = User.objects.create_user(
            username='alice',
            email='alice@example.com',
            password='cat'
        )

    def test_follow(self):
        self.u1.follow(self.u2)

        self.assertTrue(self.u1.is_following(self.u2))
        self.assertTrue(self.u2.is_followed_by(self.u1))
        self.assertFalse(self.u1.is_followed_by(self.u2))
        self.assertFalse(self.u2.is_following(self.u1)) 

    def test_unfollow(self):
        self.u1.follow(self.u2)
        self.u1.unfollow(self.u2)

        self.assertFalse(self.u1.is_following(self.u2))
        self.assertFalse(self.u2.is_followed_by(self.u1))
        self.assertFalse(self.u1.is_followed_by(self.u2))
        self.assertFalse(self.u2.is_following(self.u1)) 


class FollowsAPITests(APITestCase):
    def setUp(self):
        self.u1 = User.objects.create_user(
            username='bob',
            email='bob@example.com',
            password='dog'
        ) 

        self.u2 = User.objects.create_user(
            username='alice',
            email='alice@example.com',
            password='cat'
        ) 

    def provide_auth(self):
        credentials = base64.b64encode(b'bob:dog').decode('ascii')
        self.client.credentials(HTTP_AUTHORIZATION=f'Basic {credentials}')

        resp = self.client.post('/tokens/')
        access_token = resp.data['access_token']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

    def test_follow_user(self):
        self.provide_auth()
        user_to_follow = self.u2.id

        resp = self.client.post(f'/me/following/{user_to_follow}/')
        self.assertEqual(resp.status_code, 201) 
        self.assertTrue(self.u1.is_following(self.u2))

    def test_unfollow_user(self):
        self.provide_auth()
        self.u1.follow(self.u2)
        user_to_unfollow = self.u2.id

        resp = self.client.delete(f'/me/following/{user_to_unfollow}/')
        self.assertEqual(resp.status_code, 204)
        self.assertFalse(self.u1.is_following(self.u2))

    def test_check_if_user_is_followed_by(self):
        self.u1.follow(self.u2)
        self.provide_auth()
        user_to_check = self.u2.id

        resp = self.client.get(f'/me/following/{user_to_check}/')
        self.assertEqual(resp.status_code, 204) 

    def test_retrieve_authenticated_user_following(self):
        self.u1.follow(self.u2)
        self.provide_auth()

        resp = self.client.get('/me/following/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.data['data']), 1)
        self.assertTrue('limit' in resp.data)
        self.assertTrue('offset' in resp.data)

    def test_retrieve_authenticated_user_followers(self):
        self.u2.follow(self.u1)
        self.provide_auth()

        resp = self.client.get('/me/followers/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.data['data']), 1)
        self.assertTrue('limit' in resp.data)
        self.assertTrue('offset' in resp.data) 

    def test_retrieve_user_following(self):
        self.u1.follow(self.u2)
        user_to_find = self.u1.id

        resp = self.client.get(f'/users/{user_to_find}/following/') 
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.data['data']), 1)
        self.assertTrue('limit' in resp.data)
        self.assertTrue('offset' in resp.data) 

    def test_retrieve_user_followers(self):
        self.u2.follow(self.u1)
        user_to_find = self.u1.id

        resp = self.client.get(f'/users/{user_to_find}/followers/') 
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.data['data']), 1)
        self.assertTrue('limit' in resp.data)
        self.assertTrue('offset' in resp.data) 
