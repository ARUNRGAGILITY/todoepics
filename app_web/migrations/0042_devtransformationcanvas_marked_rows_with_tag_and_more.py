# Generated by Django 5.0.3 on 2024-03-20 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_web', '0041_currentstatedtc_futurestatedtc'),
    ]

    operations = [
        migrations.AddField(
            model_name='devtransformationcanvas',
            name='marked_rows_with_tag',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='devtransformationcanvas',
            name='marked_steps_with_star',
            field=models.TextField(blank=True, null=True),
        ),
    ]