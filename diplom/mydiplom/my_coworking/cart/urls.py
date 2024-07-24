from django.urls import path
from . import views
from .views import SearchResultsView, HomePageView

app_name = 'cart'

urlpatterns = [
	path('', views.product_list, name='product_list'),
	path('index/', views.product_list, name='catalog'),
	path('home/', views.home, name='home'),
    path('search_product/', views.search_view, name='search_product'),
	path('order/', views.order_page, name='order_date'),
	path('select_date/', views.get_available_dates, name='select_date'),
	path('cart/', views.view_cart, name='view_cart'),
	path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
	path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('select_date/', views.cart_select_date, name='cart_select_date'),
    path('checkout/', views.checkout, name='checkout'),
]
