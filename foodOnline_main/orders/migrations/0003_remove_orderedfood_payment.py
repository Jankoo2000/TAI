# Generated by Django 4.0.1 on 2023-05-05 09:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_alter_orderedfood_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderedfood',
            name='payment',
        ),
    ]
