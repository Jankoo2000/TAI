# Generated by Django 4.0.1 on 2023-05-01 18:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='quantitfy',
            new_name='quantity',
        ),
    ]
