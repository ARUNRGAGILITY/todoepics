# Generated by Django 4.2 on 2023-10-10 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_baseline', '0011_rename_name_permission_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='permission',
            name='inherit',
            field=models.BooleanField(default=False),
        ),
    ]