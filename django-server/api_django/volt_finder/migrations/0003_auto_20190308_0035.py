# Generated by Django 2.1.5 on 2019-03-08 00:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('volt_finder', '0002_remove_chargingstation_manager_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chargingstation',
            name='postal_code',
            field=models.CharField(blank=True, max_length=10),
        ),
    ]