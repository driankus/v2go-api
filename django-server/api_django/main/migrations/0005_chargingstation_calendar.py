# Generated by Django 2.1.5 on 2019-03-16 22:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0011_event_calendar_not_null'),
        ('main', '0004_auto_20190316_2110'),
    ]

    operations = [
        migrations.AddField(
            model_name='chargingstation',
            name='calendar',
            field=models.OneToOneField(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='schedule.Calendar'),
        ),
    ]
