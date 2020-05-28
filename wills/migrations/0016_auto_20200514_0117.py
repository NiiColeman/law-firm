# Generated by Django 2.2 on 2020-05-14 01:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lawyers', '0012_auto_20200422_2333'),
        ('wills', '0015_auto_20200514_0056'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='agreement',
            name='user',
        ),
        migrations.AddField(
            model_name='agreement',
            name='lawyer',
            field=models.ManyToManyField(to='lawyers.Lawyer'),
        ),
    ]
