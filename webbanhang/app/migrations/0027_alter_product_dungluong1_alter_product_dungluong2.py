# Generated by Django 5.0 on 2024-12-03 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0026_product_dungluong1_product_dungluong2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='dungluong1',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='dungluong2',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]