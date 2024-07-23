from django.test import Client, RequestFactory, TestCase
from django.urls import reverse
from .views import product_list, view_cart, add_to_cart, remove_from_cart, HomePageView, SearchResultsView, order_page, checkout, handle_payment
from .models import Product, CartItem
from django.contrib.auth.models import User
from .views import cart_select_date

class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='testpass')

        self.product1 = Product.objects.create(name='Product 1', description='Description 1', price=10.0)
        self.product2 = Product.objects.create(name='Product 2', description='Description 2', price=20.0)

        self.cart_item1 = CartItem.objects.create(user=self.user, product=self.product1, quantity=2)
        self.cart_item2 = CartItem.objects.create(user=self.user, product=self.product2, quantity=1)

    def test_product_list(self):
        request = self.factory.get(reverse('product_list'))
        request.user = self.user
        response = product_list(request)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'temp_index.html')
        self.assertIn(self.product1, response.context['products'])
        self.assertIn(self.product2, response.context['products'])

    def test_view_cart(self):
        request = self.factory.get(reverse('view_cart'))
        request.user = self.user
        response = view_cart(request)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'temp_cart.html')
        self.assertIn(self.cart_item1, response.context['cart_items'])
        self.assertIn(self.cart_item2, response.context['cart_items'])
        self.assertEqual(response.context['total_price'], 50.0)

    def test_add_to_cart(self):
        request = self.factory.get(reverse('add_to_cart', args=[self.product1.id]))
        request.user = self.user
        response = add_to_cart(request, self.product1.id)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('view_cart'))
        self.assertEqual(CartItem.objects.filter(user=self.user, product=self.product1).count(), 2)

    def test_remove_from_cart(self):
        request = self.factory.get(reverse('remove_from_cart', args=[self.cart_item1.id]))
        request.user = self.user
        response = remove_from_cart(request, self.cart_item1.id)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('view_cart'))
        self.assertEqual(CartItem.objects.filter(user=self.user, product=self.product1).count(), 0)

    def test_home_page_view(self):
        request = self.factory.get(reverse('home'))
        response = HomePageView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'temp_searchresults1.html')
        self.assertIn(self.product1, response.context['products'])
        self.assertIn(self.product2, response.context['products'])

class CartSelectDateTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_cart_select_date_post(self):
        """
        Тестирование функции cart_select_date() при POST-запросе.
        """
        data = {
            'order_day': '2023-04-01',
            'order_time': '10:00',
            'end_day': '2023-04-02',
            'end_time': '18:00'
        }
        request = self.factory.post(reverse('cart_select_date'), data)
        request.user = self.user
        response = cart_select_date(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('cart'))
        self.assertTrue(Product.objects.exists())
        self.assertTrue(CartItem.objects.exists())
        self.assertEqual(CartItem.objects.first().user, self.user)

    def test_cart_select_date_get(self):
        """
        Тестирование функции cart_select_date() при GET-запросе.
        """
        request = self.factory.get(reverse('cart_select_date'))
        request.user = self.user
        response = cart_select_date(request)

        self.assertEqual(response.status_code, 200)
    def test_search_results_view(self):
        request = self.factory.get(reverse('search_results'), {'q': 'Description'})
        response = SearchResultsView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'temp_searchresults.html')
        self.assertIn(self.product1, response.context['object_list'])
        self.assertIn(self.product2, response.context['object_list'])

    def test_order_page(self):
        request = self.factory.get(reverse('order_page'))
        request.user = self.user
        response = order_page(request)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'temp_order.html')
        self.assertIn(self.cart_item1, response.context['cart_item'])

    def test_checkout(self):
        request = self.factory.get(reverse('checkout'))
        request.user = self.user
        response = checkout(request)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'temp_cartcheckout.html')
        self.assertIn(self.cart_item1, response.context['cart_items'])
        self.assertIn(self.cart_item2, response.context['cart_items'])
        self.assertEqual(response.context['total_price'], 50.0)

    def test_handle_payment(self):
        self.cart_item1.payment_intent_id = 'test_payment_intent_id'
        self.cart_item1.save()
        request = self.factory.post(reverse('handle_payment'), {
            'payment_intent_id': 'test_payment_intent_id',
            'payment_status': 'succeeded'
        })
        response = handle_payment(request)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('cart'))
        self.cart_item1.refresh_from_db()
        self.assertEqual(self.cart_item1.payment_status, 'succeeded')
