from django.test import Client, RequestFactory, TestCase
from django.urls import reverse
from .views import feedback_view, thank_you_view
from .temp.temp import temp_feedbackform, temp_thankyou
from .forms import FeedbackForm

class ViewsTestCase(TestCase):
    def test_feedback_view(self):
        """
        Тестирование представления feedback_view
        """
        client = Client()

        response = client.get(reverse('feedback'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, temp_feedbackform)
        self.assertIsInstance(response.context['form'], FeedbackForm)

        data = {'name': 'John Doe', 'email': 'john@example.com', 'message': 'Hello, world!'}
        response = client.post(reverse('feedback'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('thank_you'))

    def test_thank_you_view(self):
        """
        Тестирование представления thank_you_view
        """
        client = Client()

        response = client.get(reverse('thank_you'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, temp_thankyou)

