# Generated by Django 4.2 on 2024-03-10 11:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_web', '0002_remove_profile_role_profile_roles'),
    ]

    operations = [
        migrations.RenameField(
            model_name='role',
            old_name='name',
            new_name='bio',
        ),
    ]