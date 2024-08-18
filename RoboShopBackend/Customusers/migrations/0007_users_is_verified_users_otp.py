# Generated by Django 5.0.7 on 2024-08-16 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Customusers', '0006_remove_users_balance_ref_alter_users_is_staff_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='users',
            name='otp',
            field=models.CharField(blank=True, max_length=4, null=True),
        ),
    ]
