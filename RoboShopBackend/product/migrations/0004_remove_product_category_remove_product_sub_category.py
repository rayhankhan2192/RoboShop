# Generated by Django 5.0.7 on 2024-08-09 16:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_rename_products_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='category',
        ),
        migrations.RemoveField(
            model_name='product',
            name='sub_category',
        ),
    ]
