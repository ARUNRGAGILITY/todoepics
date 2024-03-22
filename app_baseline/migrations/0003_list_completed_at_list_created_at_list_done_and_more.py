# Generated by Django 4.2 on 2023-09-29 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_baseline', '0002_type_list_genericpermission'),
    ]

    operations = [
        migrations.AddField(
            model_name='list',
            name='completed_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='list',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='list',
            name='done',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='list',
            name='duration_in_hours',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6),
        ),
        migrations.AddField(
            model_name='list',
            name='position',
            field=models.PositiveIntegerField(default=1000),
        ),
        migrations.AddField(
            model_name='list',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]