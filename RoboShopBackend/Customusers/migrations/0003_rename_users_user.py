# Generated by Django 5.0.7 on 2024-07-22 16:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Customusers', '0002_alter_users_managers_remove_users_phone_and_more'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Users',
            new_name='User',
        ),
    ]