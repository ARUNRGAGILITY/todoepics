# Generated by Django 4.2 on 2023-10-11 05:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_baseline', '0015_customgroup_can_add_customgroup_can_change_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customgroup',
            name='can_add',
        ),
        migrations.RemoveField(
            model_name='customgroup',
            name='can_change',
        ),
        migrations.RemoveField(
            model_name='customgroup',
            name='can_delete',
        ),
        migrations.RemoveField(
            model_name='customgroup',
            name='can_view',
        ),
    ]