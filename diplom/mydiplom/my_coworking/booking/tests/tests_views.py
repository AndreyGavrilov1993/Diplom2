from django.test import Client, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Computer, Printing, Booking
from .views import book, book_computer, book_printing
from django.test import TestCase
from datetime import datetime, timedelta

class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_book_view(self):
        '''Проверяет, что представление book возвращает правильный шаблон и статус-код.'''
        self.client.force_login(self.user)
        response = self.client.get(reverse('book'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'temp_book.html')

    def test_book_computer_view_get(self):
        '''Проверяет, что представление book_computer возвращает правильный шаблон и статус-код при GET-запросе.'''
        self.client.force_login(self.user)
        response = self.client.get(reverse('book_computer'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'temp_bookcomputer.html')

    def test_book_computer_view_post(self):
        '''Проверяет, что представление book_computer создает новую бронь компьютера при POST-запросе.'''
        self.client.force_login(self.user)
        start_date = datetime.now().date()
        end_date = start_date + timedelta(days=1)
        response = self.client.post(reverse('book_computer'), {'start_date': start_date, 'end_date': end_date})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('book'))
        self.assertTrue(Computer.objects.filter(status='occupied').exists())
        self.assertTrue(Booking.objects.filter(user=self.user, computer__isnull=False).exists())

    def test_book_printing_view_get(self):
        '''Проверяет, что book_printing возвращает правильный шаблон и статус-код при GET-запросе.'''
        self.client.force_login(self.user)
        response = self.client.get(reverse('book_printing'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'temp_bookprinting.html')

    def test_book_printing_view_post(self):
        '''Проверяет, что представление book_printing создает новую бронь печати при POST-запросе.'''
        self.client.force_login(self.user)
        start_date = datetime.now().date()
        end_date = start_date + timedelta(days=1)
        pages = 100
        response = self.client.post(reverse('book_printing'), {'start_date': start_date, 'end_date': end_date, 'pages': pages})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('book'))
        self.assertTrue(Printing.objects.filter(pages=pages).exists())
        self.assertTrue(Booking.objects.filter(user=self.user, printing__isnull=False).exists())