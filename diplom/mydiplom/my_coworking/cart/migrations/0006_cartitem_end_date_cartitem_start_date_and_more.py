# Generated by Django 4.2.7 on 2024-07-23 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0005_cartitem_payment_intent_id_cartitem_payment_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='end_date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='cartitem',
            name='start_date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='end_date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='start_date',
            field=models.DateField(null=True),
        ),
    ]
