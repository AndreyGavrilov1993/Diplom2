import datetime
from django.test import TestCase
from cart.models import Product, CartItem
from mydiplom.my_coworking.cart.models import get_available_datetime

class ProductModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        """Set up non-modified objects used by test methods."""
        Product.objects.create(name='Printer', description='Printer for printing documents')

    def test_name_label(self):
        product = Product.objects.get(id=1)
        field_label = product._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_description_label(self):
        product = Product.objects.get(id=1)
        field_label = product._meta.get_field('description').verbose_name
        self.assertEqual(field_label, 'description')

    def test_quantity_label(self):
        product = Product.objects.get(id=1)
        field_label = product._meta.get_field('quantity').verbose_name
        self.assertEqual(field_label, 'quantity')

    def test_price_label(self):
        product = Product.objects.get(id=1)
        field_label = product._meta.get_field('price').verbose_name
        self.assertEqual(field_label, 'price')

    def test_image_label(self):
        product = Product.objects.get(id=1)
        field_label = product._meta.get_field('image').verbose_name
        self.assertEqual(field_label, 'image')

    def test_name_max_length(self):
        product = Product.objects.get(id=1)
        max_length = product._meta.get_field('name').verbose_name
        self.assertEqual(max_length, 100)

    def test_price_max_digits(self):
        product = Product.objects.get(id=1)
        max_digits = product._meta.get_field('price').verbose_name
        self.assertEqual(max_digits, 10)

    def test_price_decimal_places(self):
        product = Product.objects.get(id=1)
        decimal_places = product._meta.get_field('price').verbose_name
        self.assertEqual(decimal_places, 2)

    def test_object_name_is_lastname_comma_firstname(self):
        product = Product.objects.get(id=1)
        expected_object_name = '{0}, {1}'.format(product.description, product.name)
        self.assertEqual(str(product), expected_object_name)

    def test_get_absolute_url(self):
        product = Product.objects.get(id=1)
        # This will also if the urlconf is not defined.
        self.assertEqual(product.get_absolute_url(), '/cart/index/1')

class CartItemModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        """Set up non-modified objects used by test methods."""
        CartItem.objects.create(product='Printer', quantity='1')

    def test_product_label(self):
        cart = CartItem.objects.get(id=1)
        field_label = cart._meta.get_field('product').verbose_name
        self.assertEqual(field_label, 'product')

    def test_quantity_label(self):
        cart = CartItem.objects.get(id=1)
        field_label = cart._meta.get_field('quantity').verbose_name
        self.assertEqual(field_label, 'quantity')

    def test_total_price_label(self):
        cart = CartItem.objects.get(id=1)
        field_label = cart._meta.get_field('total_price').verbose_name
        self.assertEqual(field_label, 'total price')

    def test_payment_intent_id_label(self):
        cart = CartItem.objects.get(id=1)
        field_label = cart._meta.get_field('payment_intent_id').verbose_name
        self.assertEqual(field_label, 'payment intent id')

    def test_payment_status_label(self):
        cart = CartItem.objects.get(id=1)
        field_label = cart._meta.get_field('payment_status').verbose_name
        self.assertEqual(field_label, 'payment status')

    def test_date_added_today(self):
        """Test model is valid date_added is today"""
        cart = datetime.date.today()
        field_label = cart.today().strftime('date_added').verbose_name
        self.assertEqual(field_label, 'date added')

    def test_order_day(self):
        """Test model is valid date_added is day"""
        cart = get_available_datetime()
        field_label = cart._meta.strftime('order_day').verbose_name
        self.assertEqual(field_label, 'order day')

    def test_order_time(self):
        """Test model is valid date_added is time"""
        cart = get_available_datetime()
        field_label = cart._meta.strftime('order_time').verbose_name
        self.assertEqual(field_label, 'order time')

    def test_name_max_length(self):
        cart = CartItem.objects.get(id=1)
        max_length = cart._meta.get_field('name').verbose_name
        self.assertEqual(max_length, 100)

    def test_total_price_max_digits(self):
        cart = CartItem.objects.get(id=1)
        max_digits = cart._meta.get_field('total_price').verbose_name
        self.assertEqual(max_digits, 10)

    def test_total_price_decimal_places(self):
        cart = CartItem.objects.get(id=1)
        decimal_places = cart._meta.get_field('total_price').verbose_name
        self.assertEqual(decimal_places, 2)

    def test_object_name_is_lastname_comma_firstname(self):
        cart = CartItem.objects.get(id=1)
        expected_object_name = '{0}, {1}'.format(cart.quantity, cart.product)
        self.assertEqual(str(cart), expected_object_name)

    def test_get_absolute_url(self):
        cart = CartItem.objects.get(id=1)
        # This will also if the urlconf is not defined.
        self.assertEqual(cart.get_absolute_url(), '/cart/cart/1')