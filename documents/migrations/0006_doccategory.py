# Generated by Django 2.2.6 on 2020-01-30 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0005_document_storage_location'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('date_updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Doc Category',
                'verbose_name_plural': 'Doc Categories',
            },
        ),
    ]