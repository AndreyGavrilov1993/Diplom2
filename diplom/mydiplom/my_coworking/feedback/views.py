from django.shortcuts import render, redirect
from .forms import FeedbackForm
from .temp.temp import temp_feedbackform, temp_thankyou

def feedback_view(request):
    """
    Функция обрабатывает запросы на страницу обратной связи.
    """
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('thank_you')
    else:
        form = FeedbackForm()
    return render(request, temp_feedbackform, {'form': form})

def thank_you_view(request):
    """
    Функция просто рендерит шаблон страницы "Спасибо".
    """
    return render(request, temp_thankyou)