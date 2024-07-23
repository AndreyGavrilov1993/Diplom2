import datetime
from django.utils import timezone
from django.test import TestCase
from cart.forms import DateInput, DateForm, SearchForm

class DateInputTest(TestCase):

    def test_date_input(self):
        '''Test form is invalid if input_date'''
        form = DateInput()
        self.assertEqual(form.fields['date_input'].input_type, 'date')

class DateFormTest(TestCase):

    def test_start_date_form(self):
        date = datetime.now().date()
        form_data = {'date_form': date}
        form = DateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_end_date_form(self):
        date = datetime.now().date() + datetime.timedelta(days=7)
        form_data = {'date_form': date}
        form = DateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_renew_form_date_max(self):
        date = timezone.now() + datetime.timedelta(weeks=7)
        form_data = {'renewal_date': date}
        form = DateForm(data=form_data)
        self.assertTrue(form.is_valid())

class SearchFormTest(TestCase):

    def test_query_form(self):
        form = SearchForm.objects.get(id=1)
        field_label = form._meta.get_field('query').verbose_name
        self.assertEqual(field_label, 'query')

    def test_query_max_length(self):
        form = SearchForm.objects.get(id=1)
        max_length = form._meta.get_field('query').verbose_name
        self.assertEqual(max_length, 100)
