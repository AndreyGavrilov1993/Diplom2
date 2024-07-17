from django.contrib.auth.decorators import login_required
from django.template import loader
from .models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .temp.temp import temp_login, temp_registration, temp_main, temp_users, temp_details, temp_template, temp_login1, \
    temp_all_users

@login_required
def user_login(request):
    """
    Эта функция обрабатывает процесс аутентификации пользователя.
    """
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_authenticated:
                    login(request, user)
                    return redirect('main')
                else:
                    context = {'error': 'Неправильное имя пользователя или пароль'}
                    return render(request, temp_login1, context)
            else:
                context = {'error': 'Неправильное имя пользователя или пароль'}
                return render(request, temp_login1, context)
    else:
        form = LoginForm()
    return render(request, temp_login,{'form': form})

def user_logout(redirect):
    """
    Эта функция обрабатывает процесс выхода пользователя из системы.
    """
    logout(redirect)
    return redirect('login')

def registration_view(request):
    """
    Эта функция обрабатывает процесс регистрации нового пользователя.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.firstname = form.cleaned_data.get('firstname')
            user.lastname = form.cleaned_data.get('lastname')
            user.phone = form.cleaned_data.get('phone')
            user.joined_date = form.cleaned_data.get('joined_date')
            user.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, temp_registration, {'form': form})

def main_view(request):
    """
    Эта функция просто рендерит шаблон "temp_main" и передает в него текущего пользователя.
    """
    return render(request, temp_main, {'user': request.user})

def users(request):
    """
    Эта функция получает список всех пользователей из базы данных и передает его в шаблон "temp_users" для отображения.
    """
    myusers = User.objects.all().values()
    template = loader.get_template(temp_all_users)
    context = {
        'myusers': myusers,
    }
    return HttpResponse(template.render(context, request))

def details(request, id):
    """
    Эта функция получает пользователя по его ID и передает его в шаблон "temp_details" для отображения подробной информации.
    """
    myuser = User.objects.get(id=id)
    template = loader.get_template(temp_details)
    context = {
        'myuser': myuser,
    }
    return HttpResponse(template.render(context, request))

def main(request):
    """
    Эта функция просто рендерит шаблон "temp_main".
    """
    template = loader.get_template(temp_main)
    return HttpResponse(template.render())

def testing(request):
    """
    Эта функция рендерит шаблон "temp_template" и передает в него контекст с данными о коворкинге.
    """
    template = loader.get_template(temp_template)
    context = {
        'Коворкинг': ['Рабочие места', 'Мини офисы', 'Конференц зал', 'Переговорные', 'Аренда компьютеров', 'Печать', 'Администратор'],
    }
    return HttpResponse(template.render(context, request))

def all_users(request):
    """
    Представление, которое возвращает список всех пользователей.
    """
    users = User.objects.all()
    return render(request, temp_users, {'users': users})




