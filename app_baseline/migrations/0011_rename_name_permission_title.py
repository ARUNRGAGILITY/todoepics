# Generated by Django 4.2 on 2023-10-10 11:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_baseline', '0010_permission_list_permission_work_permission'),
    ]

    operations = [
        migrations.RenameField(
            model_name='permission',
            old_name='name',
            new_name='title',
        ),
    ]
