import datetime
from django.test import TestCase
from feedback.models import Feedback

class FeedbackTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Feedback.objects.create(message='Big', rating='0')

    def test_message_label(self):
        feedback = Feedback.objects.get(id=1)
        field_label = feedback._meta.get_field('message').verbose_name
        self.assertEquals(field_label,'message')

    def test_created_add(self):
        """Test model is valid date_added is today"""
        feedback = datetime.date.today()
        field_label = feedback.today().strftime('created_add').verbose_name
        self.assertEqual(field_label, 'created add')

    def test_get_absolute_url(self):
        feedback = Feedback.objects.get(id=1)
        self.assertEquals(feedback.get_absolute_url(), '/feedback_form/1')