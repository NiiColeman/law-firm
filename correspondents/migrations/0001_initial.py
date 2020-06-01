# Generated by Django 2.2.6 on 2020-05-01 18:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cases', '0035_auto_20200427_1447'),
        ('clients', '0003_auto_20200426_1309'),
    ]

    operations = [
        migrations.CreateModel(
            name='Correspondent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('correspondent', models.CharField(max_length=250)),
                ('date_added', models.DateTimeField(auto_now=True)),
                ('description', models.TextField()),
                ('case', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cases.Case')),
                ('clients', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='clients.Client')),
                ('lawyer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Correspondent',
                'verbose_name_plural': 'Correspondents',
            },
        ),
    ]