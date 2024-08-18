# Generated by Django 5.0.7 on 2024-08-17 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Customusers', '0008_users_otp_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='is_staff',
            field=models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status'),
        ),
        migrations.AlterField(
            model_name='users',
            name='is_superuser',
            field=models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status'),
        ),
    ]