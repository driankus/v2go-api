# Generated by Django 2.1.5 on 2019-04-09 13:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('volt_reservation', '0005_auto_20190407_1625'),
        ('schedule', '0011_event_calendar_not_null'),
        ('main', '0015_ev_ev_owner'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='EV',
            new_name='ElectricVehicle',
        ),
    ]
