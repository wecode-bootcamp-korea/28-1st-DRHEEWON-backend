# Generated by Django 3.2.5 on 2022-01-05 07:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='orderitem',
            table='order_items',
        ),
    ]
