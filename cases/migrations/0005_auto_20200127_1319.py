# Generated by Django 2.2.6 on 2020-01-27 21:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0004_auto_20200123_0300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='case',
            name='attachments',
            field=models.FileField(blank=True, max_length=300, null=True, upload_to='attachements/'),
        ),
    ]
