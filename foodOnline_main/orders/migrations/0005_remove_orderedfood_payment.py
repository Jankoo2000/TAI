# Generated by Django 4.0.1 on 2023-05-05 09:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_orderedfood_payment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderedfood',
            name='payment',
        ),
    ]
