# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class Computer(models.Model):
    STATUS_CHOICES = (
        ('available', 'Available'),
        ('occupied', 'Occupied'),
    )
    id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    start_date = models.DateField()
    end_date = models.DateField()

class Printing(models.Model):
    id = models.AutoField(primary_key=True)
    pages = models.PositiveIntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    free_limit = models.PositiveIntegerField(default=50)

class Booking(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    computer = models.ForeignKey(Computer, on_delete=models.CASCADE, null=True, blank=True)
    printing = models.ForeignKey(Printing, on_delete=models.CASCADE, null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
