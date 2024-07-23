from django.test import TestCase
from django.contrib.auth.models import User
from .models import Computer, Printing, Booking

class ComputerModelTestCase(TestCase):
    def test_computer_status(self):
        computer = Computer.objects.create(status='available')
        self.assertEqual(computer.status, 'available')

        computer.status = 'occupied'
        computer.save()
        self.assertEqual(computer.status, 'occupied')

class PrintingModelTestCase(TestCase):
    def test_printing_pages(self):
        printing = Printing.objects.create(pages=100, start_date='2023-04-01', end_date='2023-04-30')
        self.assertEqual(printing.pages, 100)
        self.assertEqual(printing.free_limit, 50)

class BookingModelTestCase(TestCase):
    def test_booking_user_and_computer(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        computer = Computer.objects.create(status='available')
        booking = Booking.objects.create(user=user, computer=computer, start_date='2023-04-01', end_date='2023-04-05')

        self.assertEqual(booking.user, user)
        self.assertEqual(booking.computer, computer)