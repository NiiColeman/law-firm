# Generated by Django 2.2 on 2020-05-06 23:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wills', '0012_remove_agreement_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='agreement',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='wills.AgreementCategory'),
        ),
    ]