# Generated by Django 5.0.7 on 2024-08-16 18:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_alter_product_category_alter_product_sub_category'),
    ]

    operations = [
        migrations.DeleteModel(
            name='HomePage',
        ),
        migrations.DeleteModel(
            name='HomeSlide',
        ),
        migrations.DeleteModel(
            name='Specialoffer',
        ),
    ]
