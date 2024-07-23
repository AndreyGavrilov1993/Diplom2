from ..temp.temp import temp_main, temp_users
from django.test import Client, RequestFactory, TestCase
from django.urls import reverse
from .views import (
    user_login, user_logout, registration_view, main_view, users, details, main, testing, all_users
)
from .models import User
from django.contrib.auth.models import AnonymousUser

class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='testuser', password='testpassword'
        )

    def test_user_login(self):
        request = self.factory.post(reverse('login'), {'username': 'testuser', 'password': 'testpassword'})
        request.user = self.user
        response = user_login(request)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('main'))

    def test_user_logout(self):
        request = self.factory.get(reverse('logout'))
        request.user = self.user
        response = user_logout(request)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

    def test_registration_view(self):
        request = self.factory.post(reverse('register'), {
            'username': 'newuser', 'password1': 'newpassword', 'password2': 'newpassword'
        })
        response = registration_view(request)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

    def test_main_view(self):
        request = self.factory.get(reverse('main'))
        request.user = self.user
        response = main_view(request)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, temp_main)

    def test_users(self):
        request = self.factory.get(reverse('users'))
        request.user = self.user
        response = users(request)
        self.assertEqual(response.status_code, 200)

    def test_details(self):
        request = self.factory.get(reverse('details', args=[self.user.id]))
        request.user = self.user
        response = details(request, self.user.id)
        self.assertEqual(response.status_code, 200)

    def test_main(self):
        request = self.factory.get(reverse('main'))
        response = main(request)
        self.assertEqual(response.status_code, 200)

    def test_testing(self):
        request = self.factory.get(reverse('testing'))
        response = testing(request)
        self.assertEqual(response.status_code, 200)

    def test_all_users(self):
        request = self.factory.get(reverse('all_users'))
        request.user = self.user
        response = all_users(request)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, temp_users)