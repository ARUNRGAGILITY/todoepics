# Generated by Django 4.2 on 2024-03-11 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_web', '0006_alter_role_options_profile_active_profile_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='role',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
