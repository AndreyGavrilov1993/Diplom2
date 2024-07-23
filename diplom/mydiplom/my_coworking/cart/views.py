from itertools import product

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
# Create your views here.
from django.shortcuts import redirect
from .models import Product, CartItem
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.views.generic import TemplateView, ListView
from . import models
from datetime import datetime, timedelta
from django.shortcuts import render
from .forms import SearchForm
from .utils import search_product
from .temp.temp import temp_index, temp_cart, temp_searchresults, temp_searchresults1, \
    temp_products, temp_order, temp_checkout, temp_searchproduct, temp_cartcheckout
from django.contrib import messages

def product_list(request):
    """
    Эта функция отвечает за отображение списка всех продуктов на странице каталога.
    Она получает все объекты модели Product и передает их в шаблон temp_index.
    """
    products = Product.objects.all()
    return render(request, temp_index, {'products': products})

def view_cart(request):
    """
    Эта функция отвечает за отображение корзины пользователя.
    Она получает все объекты модели CartItem, связанные с текущим пользователем,
    и вычисляет общую стоимость всех товаров в корзине.
    Затем она передает эти данные в шаблон temp_cart.
    """
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, temp_cart, {'cart_items': cart_items, 'total_price': total_price})

def add_to_cart(request, product_id):
    """
    Эта функция отвечает за добавление продукта в корзину пользователя.
    Она получает идентификатор продукта, находит соответствующий объект Product
    и создает или обновляет объект CartItem для текущего пользователя.
    """
    product = Product.objects.get(id=product_id)
    cart_item, created = CartItem.objects.get_or_create(product=product,
                                                    user=request.user)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart:view_cart')

def remove_from_cart(request, item_id):
    """
    Эта функция отвечает за удаление товара из корзины пользователя.
    Она получает идентификатор товара в корзине и удаляет соответствующий объект CartItem.
    """
    cart_item = CartItem.objects.get(id=item_id)
    cart_item.delete()
    return redirect('cart:view_cart')

class HomePageView(TemplateView):
    """
    Этот класс отвечает за отображение результатов поиска на главной странице.
    Он получает параметры поиска из запроса и фильтрует продукты соответствующим образом,
    передавая их в шаблон temp_searchresults1.
    """
    template_name = temp_searchresults1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_by = self.request.GET.get('search_by')
        query = self.request.GET.get('query')
        search_message = "All Product"
        if search_by in ['name'] and query:
            if search_by == 'name':
                search_message = f'Searching for "name" by {query}'
                products = models.Product.objects.filter(name__icontains=query)
                context['search_message'] = search_message
                context['products'] = products
                return context
        context['search_message'] = search_message
        context['products'] = models.Product.objects.all()
        return context

class SearchResultsView(ListView):
    """
    Этот класс отвечает за отображение результатов расширенного поиска.
    Он использует модуль django.contrib.postgres.search для выполнения
    полнотекстового поиска по описанию и названию продуктов,
    сортируя результаты по релевантности.
    """
    model = Product
    template_name = temp_searchresults
    def get_queryset(self):
        query = self.request.GET.get('q')
        search_vector = SearchVector('description', weight='B') + SearchVector('name', weight='A')
        search_query = SearchQuery(query)
        return (self.model.objects.annotate(rank=SearchRank(search_vector, search_query)).filter(rank__gte=0.3).order_by('-rank'))

def home(request):
    return HttpResponse('Hello, World!')

def get_available_dates():
    """
    Функция возвращает список доступных дат и времени для заказа.
    Она анализирует все существующие заказы, чтобы определить занятые временные интервалы,
    и генерирует список доступных дат и времени.
    """
    # Получаем все существующие заказы
    cart_items = CartItem.objects.all()
    # Создаем словарь, где ключ - дата, а значение - список занятых временных интервалов
    occupied_slots = {}
    for item in cart_items:
        date = item.order_day
        time = item.order_time
        if date not in occupied_slots:
            occupied_slots[date] = []
        occupied_slots[date].append(time)
    # Генерируем список доступных дат и времени
    available_dates = []
    start_date = datetime.now().date()
    end_date = start_date + timedelta(days=7)  # Ограничиваем диапазон на 7 дней
    while start_date <= end_date:
        available_times = ['08:00', '09:00', '10:00', '11:00',
                           '12:00', '13:00', '14:00', '15:00',
                           '16:00', '17:00', '18:00', '19:00',]
        if start_date not in occupied_slots:
            available_dates.append((start_date, available_times))
        else:
            occupied_times = occupied_slots[start_date]
            for time in available_times:
                if time not in occupied_times:
                    available_dates.append((start_date, [time]))
        start_date += timedelta(days=1)
    return available_dates

@login_required
def cart_select_date(request):
    if request.method == 'POST':
        order_day = request.POST['order_day']
        order_time = request.POST['order_time']
        end_day = request.POST['end_day']
        end_time = request.POST['end_time']
        product = Product.objects.create(order_day=order_day, order_time=order_time, end_day=end_day, end_time=end_time)
        cart_item = CartItem.objects.create(user=request.user, product=product, order_day=order_day, order_time=order_time, end_day=end_day, end_time=end_time)
        messages.success(request, 'Product successfully added to your shopping cart.')
        return redirect('cart')
    return render(request, temp_cart)

def search_view(request):
    """
    Представление для страницы результатов поиска.
    """
    form = SearchForm(request.GET or None)
    if form.is_valid():
        query = form.cleaned_data['query']
        products = search_product(query)
    else:
        products = []
    return render(request, temp_searchproduct, {
        'form': form,
        'products': products
    })

def order_page(request):
    """
    Эта функция отвечает за отображение страницы оформления заказа.
    Она получает выбранные дату и время заказа из формы и сохраняет их в объекте CartItem.
    """
    if request.method == 'POST':
        order_day = request.POST['order_day']
        order_time = request.POST['order_time']
        # Обработка данных заказа и сохранение в базу данных
        cart_item = CartItem.objects.create(
            product=product,
            user=request.user,
            order_day=order_day,
            order_time=order_time,
        )
        cart_item.save()
        return redirect('cart')
    else:
        cart_item = CartItem.objects.filter(user=request.user).first()
        return render(request, temp_order, {'cart_item': cart_item})

def checkout(request):
    """
    Эта функция отвечает за отображение страницы оформления заказа.
    Она получает все незавершенные заказы пользователя,
    вычисляет общую стоимость, и в случае успешной оплаты обновляет статус заказа.
    """
    cart_items = CartItem.objects.filter(user=request.user, payment_status="unpaid")
    total_price = sum(item.get_total_price() for item in cart_items)
    if request.method == "POST":
        for item in cart_items:
            client_secret = item.create_payment_intent()
            context = {
                "client_secret": client_secret,
                "cart_items": cart_items,
                "total_price": total_price,
            }
            return render(request, temp_checkout, context)
    context = {
        "cart_items": cart_items,
        "total_price": total_price,
    }
    return render(request, temp_cartcheckout, context)

def handle_payment(request):
    """
    Эта функция отвечает за обработку платежа.
    Она получает идентификатор платежного намерения и статус платежа,
    и обновляет соответствующий объект CartItem.
    """
    payment_intent_id = request.POST.get("payment_intent_id")
    payment_status = request.POST.get("payment_status")
    try:
        cart_item = CartItem.objects.get(payment_intent_id=payment_intent_id)
        cart_item.update_payment_status(payment_status)
        return redirect("cart")
    except CartItem.DoesNotExist:
        return redirect("checkout")




