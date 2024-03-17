# Generated by Django 4.2 on 2024-03-16 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_web', '0033_safetype_organization'),
    ]

    operations = [
        migrations.AlterField(
            model_name='capability',
            name='deleted',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='epic',
            name='deleted',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='feature',
            name='deleted',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='keyresult',
            name='deleted',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='objective',
            name='deleted',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='deleted',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='quarterlymeasure',
            name='deleted',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='safetype',
            name='deleted',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='spike',
            name='deleted',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='strategictheme',
            name='deleted',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='deleted',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='userstory',
            name='deleted',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]