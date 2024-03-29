# Generated by Django 5.0.3 on 2024-03-27 06:17

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_baseline', '0028_typetype_type_type_type'),
        ('app_web', '0048_remove_mappingwbs_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='strategictheme',
            name='corresponding_mptt_id',
            field=models.ForeignKey(default=django.utils.timezone.now, on_delete=django.db.models.deletion.CASCADE, related_name='app_web_strategic_themes', to='app_baseline.list'),
            preserve_default=False,
        ),
    ]
