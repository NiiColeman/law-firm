# Generated by Django 2.2.6 on 2020-01-28 16:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0010_case_attachments'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='case',
            name='attachments',
        ),
    ]
