# Generated by Django 5.0 on 2024-12-03 13:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0027_alter_product_dungluong1_alter_product_dungluong2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='dungluong1',
        ),
        migrations.RemoveField(
            model_name='product',
            name='dungluong2',
        ),
    ]