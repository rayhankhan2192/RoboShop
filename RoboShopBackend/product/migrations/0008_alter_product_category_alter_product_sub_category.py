# Generated by Django 5.0.7 on 2024-08-14 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0007_remove_category_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ManyToManyField(blank=True, to='product.category'),
        ),
        migrations.AlterField(
            model_name='product',
            name='sub_category',
            field=models.ManyToManyField(blank=True, to='product.sub_category'),
        ),
    ]