# Generated by Django 2.2.6 on 2020-03-05 05:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0019_remove_document_files'),
    ]

    operations = [
        migrations.AddField(
            model_name='docfile',
            name='document',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='documents.Document'),
        ),
    ]