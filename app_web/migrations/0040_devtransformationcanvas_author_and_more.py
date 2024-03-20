# Generated by Django 5.0.3 on 2024-03-20 10:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_web', '0039_devtransformationcanvas_boundaries_and_constraints_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='devtransformationcanvas',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='authdevcanvas', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='opstransformationcanvas',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='authopscanvas', to=settings.AUTH_USER_MODEL),
        ),
    ]
