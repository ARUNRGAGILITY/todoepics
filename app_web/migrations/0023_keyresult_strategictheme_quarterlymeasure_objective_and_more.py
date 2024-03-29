# Generated by Django 4.2 on 2024-03-13 13:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_web', '0022_remove_valuestreamsteps_content_type_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='KeyResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.PositiveIntegerField(default=1000)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(blank=True, default=True, null=True)),
                ('name', models.CharField(max_length=255)),
                ('target', models.TextField(blank=True, null=True)),
            ],
            options={
                'ordering': ['position'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StrategicTheme',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.PositiveIntegerField(default=1000)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(blank=True, default=True, null=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'ordering': ['position'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='QuarterlyMeasure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.PositiveIntegerField(default=1000)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(blank=True, default=True, null=True)),
                ('quarter', models.CharField(choices=[('Q1', 'Q1'), ('Q2', 'Q2'), ('Q3', 'Q3'), ('Q4', 'Q4')], max_length=2)),
                ('year', models.PositiveIntegerField(blank=True, null=True)),
                ('value', models.TextField(blank=True, null=True)),
                ('key_result', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quarterly_measures', to='app_web.keyresult')),
            ],
            options={
                'ordering': ['position'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Objective',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.PositiveIntegerField(default=1000)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(blank=True, default=True, null=True)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('theme', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='objectives', to='app_web.strategictheme')),
            ],
            options={
                'ordering': ['position'],
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='keyresult',
            name='objective',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='key_results', to='app_web.objective'),
        ),
    ]
