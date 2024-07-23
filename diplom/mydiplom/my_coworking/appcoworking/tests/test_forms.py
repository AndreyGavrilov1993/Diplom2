from django.test import TestCase
from appcoworking.forms import LoginForm

class LoginFormTest(TestCase):

    def test_username_label(self):
        form = LoginForm.objects.get(id=1)
        field_label = form._meta.get_field('username').verbose_name
        self.assertEqual(field_label, 'username')

    def test_password_label(self):
        form = LoginForm.objects.get(id=1)
        field_label = form._meta.get_field('password').verbose_name
        self.assertEqual(field_label, 'password')