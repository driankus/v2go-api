# Generated by Django 2.1.5 on 2019-04-07 14:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_chargingstation_cs_host'),
    ]

    operations = [
        migrations.AddField(
            model_name='ev',
            name='ev_owner',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
