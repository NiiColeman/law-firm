# Generated by Django 2.2.6 on 2020-04-28 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedules', '0006_meetingsession_room'),
    ]

    operations = [
        migrations.AddField(
            model_name='meetingsession',
            name='expired',
            field=models.BooleanField(default=False),
        ),
    ]