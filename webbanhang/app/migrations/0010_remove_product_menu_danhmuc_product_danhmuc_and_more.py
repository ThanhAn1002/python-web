# Generated by Django 5.0 on 2024-11-25 17:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_remove_product_danhmuc_menu_product_menu_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='menu',
        ),
        migrations.CreateModel(
            name='DanhMuc',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_sub', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=200, null=True)),
                ('slug', models.SlugField(max_length=200, unique=True)),
                ('sub_danhmuc', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sub_danhmuc_s', to='app.danhmuc')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='danhmuc',
            field=models.ManyToManyField(related_name='product', to='app.danhmuc'),
        ),
        migrations.DeleteModel(
            name='Menu',
        ),
    ]
