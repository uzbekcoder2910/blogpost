from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Post

# Create your tests here.
class PostModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            username="testuser",
            email="testuser1@gmail.com",
            password="secret1",
        )

        self.post = Post.objects.create(
            title="testpost",
            body="test body",
            author=self.user,

        )

    def test_string_representation(self):
        self.assertEqual(str(self.post), self.post.title)

    def test_post_content(self):
        self.assertEqual(f'{self.post.title}', 'testpost')
        self.assertEqual(f'{self.post.body}', 'test body')
        self.assertEqual(f'{self.user}', 'testuser')


    def test_post_list_view(self):
        response = self.client.get(reverse('post-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.title)
        self.assertContains(response, self.post.body)
        self.assertTemplateUsed(response, 'home.html')

    def post_detail_view(self):
        response = self.client.get(reverse('post_detail', kwargs={'pk': self.post.pk}))
        no_response = self.client.get(reverse('post_detail', kwargs={'pk': 10000}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, self.post.title)
        self.assertTemplateUsed(response, 'post_detail.html')
