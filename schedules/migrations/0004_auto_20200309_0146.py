# Generated by Django 2.2.6 on 2020-03-09 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedules', '0003_schedule'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='start_time',
            field=models.DateTimeField(),
        ),
    ]