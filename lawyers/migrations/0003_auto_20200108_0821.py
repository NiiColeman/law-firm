# Generated by Django 2.2.6 on 2020-01-08 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lawyers', '0002_auto_20200108_0811'),
    ]

    operations = [
        migrations.AlterField(
            model_name='role',
            name='id',
            field=models.PositiveSmallIntegerField(choices=[(1, 'clerk'), (2, 'front desk'), (3, 'secretary')], primary_key=True, serialize=False),
        ),
    ]