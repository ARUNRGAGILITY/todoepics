# Generated by Django 5.0.3 on 2024-03-28 17:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_web', '0058_remove_capability_epic_remove_component_epic_and_more'),
        ('app_xpresskanban', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='work_item_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='xpress_org_witype1', to='app_xpresskanban.type_hsdb'),
        ),
    ]
