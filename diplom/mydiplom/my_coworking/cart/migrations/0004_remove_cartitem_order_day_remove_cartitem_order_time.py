# Generated by Django 4.2.7 on 2024-07-07 22:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0003_alter_cartitem_options_cartitem_order_day_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='order_day',
        ),
        migrations.RemoveField(
            model_name='cartitem',
            name='order_time',
        ),
    ]