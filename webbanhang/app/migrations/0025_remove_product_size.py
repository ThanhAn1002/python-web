# Generated by Django 5.0 on 2024-12-03 13:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0024_product_size'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='size',
        ),
    ]