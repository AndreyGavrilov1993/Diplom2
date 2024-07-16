from django import forms

class DateInput(forms.DateInput):
    input_type = 'date'

class DateForm(forms.Form):
    start_date = forms.DateField(widget=DateInput)
    end_date = forms.DateField(widget=DateInput)

class SearchForm(forms.Form):
    query = forms.CharField(label='Поиск', max_length=100)