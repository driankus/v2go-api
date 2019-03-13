# Generated by Django 2.1.5 on 2019-03-12 22:35

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChargingStation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nk', models.CharField(db_index=True, max_length=32, unique=True)),
                ('name', models.CharField(blank=True, max_length=255)),
                ('external_id', models.CharField(blank=True, max_length=100)),
                ('charge_level', models.CharField(choices=[('LEVEL_1', 'LEVEL_1'), ('LEVEL_2', 'LEVEL_2'), ('FAST_DC', 'FAST_DC')], default='LEVEL_2', max_length=32)),
                ('tarif_text', models.CharField(blank=True, max_length=100)),
                ('address', models.CharField(max_length=150)),
                ('location', models.CharField(default='', max_length=150)),
                ('city', models.CharField(blank=True, max_length=50)),
                ('province', models.CharField(blank=True, max_length=50)),
                ('country', models.CharField(blank=True, max_length=50)),
                ('postal_code', models.CharField(blank=True, max_length=10)),
                ('lat', models.FloatField(blank=True, null=True)),
                ('lng', models.FloatField(blank=True, null=True)),
                ('geo_location', django.contrib.gis.db.models.fields.PointField(null=True, srid=4326)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]