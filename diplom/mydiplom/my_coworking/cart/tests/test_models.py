from django.test import TestCase
from django.contrib.auth.models import User
from .models import Product, CartItem
from datetime import datetime, timedelta

class ProductModelTestCase(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Test Product",
            description="This is a test product.",
            quantity=10,
            price=9.99,
            image="test_image.jpg"
        )

    def test_product_creation(self):
        self.assertEqual(self.product.name, "Test Product")
        self.assertEqual(self.product.description, "This is a test product.")
        self.assertEqual(self.product.quantity, 10)
        self.assertEqual(self.product.price, 9.99)
        self.assertEqual(self.product.image, "test_image.jpg")

    def test_product_str_representation(self):
        self.assertEqual(str(self.product), "Test Product")

class CartItemModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.product = Product.objects.create(
            name="Test Product",
            description="This is a test product.",
            quantity=10,
            price=9.99,
            image="test_image.jpg"
        )
        self.cart_item = CartItem.objects.create(
            product=self.product,
            quantity=2,
            user=self.user,
            total_price=19.98
        )

    def test_cart_item_creation(self):
        self.assertEqual(self.cart_item.product, self.product)
        self.assertEqual(self.cart_item.quantity, 2)
        self.assertEqual(self.cart_item.user, self.user)
        self.assertEqual(self.cart_item.total_price, 19.98)

    def test_cart_item_str_representation(self):
        self.assertEqual(str(self.cart_item), "2 x Test Product")

    def test_get_total_price(self):
        self.assertEqual(self.cart_item.get_total_price(), 19.98)

    def test_create_payment_intent(self):
        client_secret = self.cart_item.create_payment_intent()
        self.assertIsNotNone(client_secret)
        self.assertIsNotNone(self.cart_item.payment_intent_id)

    def test_update_payment_status(self):
        self.cart_item.update_payment_status("paid")
        self.assertEqual(self.cart_item.payment_status, "paid")
