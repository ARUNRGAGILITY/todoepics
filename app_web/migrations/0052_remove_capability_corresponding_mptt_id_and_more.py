# Generated by Django 5.0.3 on 2024-03-27 06:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_web', '0051_remove_strategictheme_corresponding_mptt_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='capability',
            name='corresponding_mptt_id',
        ),
        migrations.RemoveField(
            model_name='component',
            name='corresponding_mptt_id',
        ),
        migrations.RemoveField(
            model_name='epic',
            name='corresponding_mptt_id',
        ),
        migrations.RemoveField(
            model_name='feature',
            name='corresponding_mptt_id',
        ),
        migrations.RemoveField(
            model_name='spike',
            name='corresponding_mptt_id',
        ),
        migrations.RemoveField(
            model_name='task',
            name='corresponding_mptt_id',
        ),
        migrations.RemoveField(
            model_name='userstory',
            name='corresponding_mptt_id',
        ),
    ]
