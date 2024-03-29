# Generated by Django 5.0.3 on 2024-03-26 11:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_baseline', '0027_alter_project_end_date_alter_project_start_date'),
        ('app_web', '0046_mappingwbs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mappingwbs',
            name='list',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app_baseline.list'),
        ),
        migrations.AlterField(
            model_name='mappingwbs',
            name='type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app_baseline.type'),
        ),
    ]
