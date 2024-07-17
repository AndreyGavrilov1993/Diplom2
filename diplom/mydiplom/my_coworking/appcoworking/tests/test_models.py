from django.test import TestCase

from appcoworking.models import User

class UserModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        """Set up non-modified objects used by test methods."""
        User.objects.create(firstname='Andrey', lastname='Gavrilov')

    def test_first_name_label(self):
        user = User.objects.get(id=1)
        field_label = user._meta.get_field('firstname').verbose_name
        self.assertEqual(field_label, 'first name')

    def test_last_name_label(self):
        user = User.objects.get(id=1)
        field_label = user._meta.get_field('lastname').verbose_name
        self.assertEqual(field_label, 'last name')

    def test_phone_label(self):
        user = User.objects.get(id=1)
        field_label = user._meta.get_field('phone').verbose_name
        self.assertEqual(field_label, 'phone')

    def test_joined_date_label(self):
        user = User.objects.get(id=1)
        field_label = user._meta.get_field('joined_date').verbose_name
        self.assertEqual(field_label, 'joined date')

    def test_firstname_max_length(self):
        user = User.objects.get(id=1)
        max_length = user._meta.get_field('firstname').verbose_name
        self.assertEqual(max_length, 255)

    def test_lastname_max_length(self):
        user = User.objects.get(id=1)
        max_length = user._meta.get_field('lastname').verbose_name
        self.assertEqual(max_length, 255)

    def test_object_firstname_is_lastname_comma_firstname(self):
        user = User.objects.get(id=1)
        expected_object_name = '{0}, {1}'.format(user.lastname, user.firstname)
        self.assertEqual(str(user), expected_object_name)

    def test_get_absolute_url(self):
        user = User.objects.get(id=1)
        # This will also if the urlconf is not defined.
        self.assertEqual(user.get_absolute_url(), '/appcoworking/user/1')