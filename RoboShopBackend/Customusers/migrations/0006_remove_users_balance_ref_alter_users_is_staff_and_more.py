# Generated by Django 5.0.7 on 2024-08-16 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Customusers', '0005_alter_users_phone'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='users',
            name='balance_ref',
        ),
        migrations.AlterField(
            model_name='users',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='users',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='users',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
