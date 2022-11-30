import base64

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APITestCase

from .models import Post
from .serializers import PostCreateSerializer

User = get_user_model()


class PostModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='bob',
            email='bob@example.com',
            password='dog'
        ) 

        self.post = Post.objects.create(
            title='Post title',
            content='Post content',
            author=self.user
        )

    def test_post_model(self):
        self.assertEqual(self.post.title, 'Post title')
        self.assertEqual(self.post.content, 'Post content')
        self.assertEqual(self.post.author, self.user)
    

class PostSerializerTests(TestCase):
    def test_valid_data(self):
        data = {
            'title': 'Valid title',
            'content': 'Valid content'
        } 

        serializer = PostCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_data(self):
        data = {
            'title': None
        } 

        serializer = PostCreateSerializer(data=data)
        self.assertFalse(serializer.is_valid())


class PostAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='bob',
            email='bob@example.com',
            password='dog'
        )

        self.post = Post.objects.create(
            title='Post title',
            content='Post content',
            author=self.user
        )

    def provide_auth(self):
        credentials = base64.b64encode(b'bob:dog').decode('ascii')
        self.client.credentials(HTTP_AUTHORIZATION=f'Basic {credentials}')

        resp = self.client.post('/tokens/')
        access_token = resp.data['access_token']

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

    def test_create_new_post(self):
        self.provide_auth()

        data = {
            'title': 'New title',
            'content': 'New content'
        }

        resp = self.client.post('/posts/', data)
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.data['title'], 'New title')
        self.assertEqual(resp.data['content'], 'New content')
        self.assertEqual(resp.data['author']['username'], 'bob')
        self.assertEqual(Post.objects.count(), 2)

    def test_retrieve_all_posts(self):
        resp = self.client.get('/posts/')

        self.assertEqual(resp.status_code, 200)
        self.assertTrue('limit' in resp.data)
        self.assertTrue('offset' in resp.data)
        self.assertEqual(len(resp.data['data']), 1)

    def test_retrieve_post_by_id(self):
        last_post = Post.objects.last()
        resp = self.client.get(f'/posts/{last_post.id}/')

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['title'],  'Post title')
        self.assertEqual(resp.data['author']['username'], 'bob')

    def test_edit_post_information(self):
        self.provide_auth()

        data = {
            'title': 'Edited title',
            'content': 'Edited content'
        } 

        last_post = Post.objects.last()
        resp = self.client.put(f'/posts/{last_post.id}/', data)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['title'], 'Edited title')
        self.assertEqual(resp.data['content'], 'Edited content')

    def test_delete_post(self):
        self.provide_auth()

        last_post = Post.objects.last()
        resp = self.client.delete(f'/posts/{last_post.id}/')

        self.assertEqual(resp.status_code, 204)
        self.assertEqual(Post.objects.count(), 0)

    def test_retrieve_all_user_posts(self):
        resp = self.client.get('/users/bob/posts/')

        self.assertEqual(resp.status_code, 200)
        self.assertTrue('limit' in resp.data)
        self.assertTrue('offset' in resp.data)
        self.assertEqual(len(resp.data['data']), 1)
