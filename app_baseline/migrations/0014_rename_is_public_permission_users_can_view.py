# Generated by Django 4.2 on 2023-10-11 05:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_baseline', '0013_permission_is_public'),
    ]

    operations = [
        migrations.RenameField(
            model_name='permission',
            old_name='is_public',
            new_name='users_can_view',
        ),
    ]
