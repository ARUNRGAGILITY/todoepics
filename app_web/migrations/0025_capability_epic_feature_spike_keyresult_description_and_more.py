# Generated by Django 4.2 on 2024-03-13 15:38

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app_web', '0024_quarterlymeasure_percentage'),
    ]

    operations = [
        migrations.CreateModel(
            name='Capability',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('position', models.PositiveIntegerField(default=1000)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(blank=True, default=True, null=True)),
                ('type', models.CharField(choices=[('EN', 'Enabler'), ('BU', 'Business')], default='BU', max_length=2)),
            ],
            options={
                'ordering': ['position'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Epic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('position', models.PositiveIntegerField(default=1000)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(blank=True, default=True, null=True)),
                ('type', models.CharField(choices=[('EN', 'Enabler'), ('BU', 'Business')], default='BU', max_length=2)),
                ('theme', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='epics', to='app_web.strategictheme')),
            ],
            options={
                'ordering': ['position'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('position', models.PositiveIntegerField(default=1000)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(blank=True, default=True, null=True)),
                ('type', models.CharField(choices=[('EN', 'Enabler'), ('BU', 'Business')], default='BU', max_length=2)),
                ('epic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='features', to='app_web.epic')),
            ],
            options={
                'ordering': ['position'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Spike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('position', models.PositiveIntegerField(default=1000)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(blank=True, default=True, null=True)),
                ('parent_capability', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='spikes', to='app_web.capability')),
                ('parent_feature', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='spikes', to='app_web.feature')),
            ],
            options={
                'ordering': ['position'],
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='keyresult',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='objective',
            name='name',
            field=models.CharField(default=django.utils.timezone.now, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='quarterlymeasure',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='quarterlymeasure',
            name='name',
            field=models.CharField(default=django.utils.timezone.now, max_length=255),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='UserStory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('position', models.PositiveIntegerField(default=1000)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(blank=True, default=True, null=True)),
                ('parent_capability', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_stories', to='app_web.capability')),
                ('parent_feature', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_stories', to='app_web.feature')),
            ],
            options={
                'ordering': ['position'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('position', models.PositiveIntegerField(default=1000)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(blank=True, default=True, null=True)),
                ('parent_spike', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='app_web.spike')),
                ('parent_story', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='app_web.userstory')),
            ],
            options={
                'ordering': ['position'],
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='capability',
            name='epic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='capabilities', to='app_web.epic'),
        ),
    ]
