# Generated by Django 5.0.6 on 2024-05-26 05:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CO2Emmision',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField()),
                ('unit', models.CharField(default='tons', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='ComponentStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('typeName', models.CharField(max_length=50)),
                ('activeCount', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='EnergyEfficiency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField()),
                ('unit', models.CharField(default='%', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='FireWall',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='GridData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_value', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Honeypot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.IntegerField()),
                ('active', models.IntegerField()),
                ('detections', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Ids',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Metric',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField()),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='SecurityAlert',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.GenericIPAddressField()),
                ('is_read', models.BooleanField()),
                ('description', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='UtilityStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='GridStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.ManyToManyField(to='dashboard.griddata')),
            ],
        ),
        migrations.CreateModel(
            name='GenerationData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('solar_plants', models.ManyToManyField(related_name='solar_metrics', to='dashboard.metric')),
                ('utility', models.ManyToManyField(related_name='utility_metrics', to='dashboard.metric')),
                ('wind_turbines_plants', models.ManyToManyField(related_name='wind_metrics', to='dashboard.metric')),
            ],
        ),
        migrations.CreateModel(
            name='ConsumptionData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commercial', models.ManyToManyField(related_name='commercial_metrics', to='dashboard.metric')),
                ('industrial', models.ManyToManyField(related_name='industrial_metrics', to='dashboard.metric')),
                ('residential', models.ManyToManyField(related_name='residential_metrics', to='dashboard.metric')),
            ],
        ),
        migrations.CreateModel(
            name='WeeklyData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('totalWeeklyValue', models.IntegerField()),
                ('data', models.ManyToManyField(to='dashboard.metric')),
            ],
        ),
        migrations.CreateModel(
            name='DashboardData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active_components', models.ManyToManyField(to='dashboard.componentstatus')),
                ('co2_emission', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='dashboard.co2emmision')),
                ('energy_efficiency', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='dashboard.energyefficiency')),
                ('firewall', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='dashboard.firewall')),
                ('grid_status', models.ManyToManyField(to='dashboard.gridstatus')),
                ('honeypot', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='dashboard.honeypot')),
                ('ids', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='dashboard.ids')),
                ('security_alerts', models.ManyToManyField(to='dashboard.securityalert')),
                ('utility_status', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='dashboard.utilitystatus')),
                ('weekly_data', models.ManyToManyField(to='dashboard.weeklydata')),
            ],
        ),
    ]
