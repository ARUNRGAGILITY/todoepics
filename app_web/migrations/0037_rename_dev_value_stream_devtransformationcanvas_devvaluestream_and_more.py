# Generated by Django 5.0.3 on 2024-03-19 17:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_web', '0036_devtransformationcanvas_opstransformationcanvas'),
    ]

    operations = [
        migrations.RenameField(
            model_name='devtransformationcanvas',
            old_name='dev_value_stream',
            new_name='devvaluestream',
        ),
        migrations.RenameField(
            model_name='opstransformationcanvas',
            old_name='ops_value_stream',
            new_name='opsvaluestream',
        ),
    ]
