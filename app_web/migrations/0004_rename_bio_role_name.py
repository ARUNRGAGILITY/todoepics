# Generated by Django 4.2 on 2024-03-10 11:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_web', '0003_rename_name_role_bio'),
    ]

    operations = [
        migrations.RenameField(
            model_name='role',
            old_name='bio',
            new_name='name',
        ),
    ]