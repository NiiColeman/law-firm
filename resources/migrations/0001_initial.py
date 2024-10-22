# Generated by Django 2.2 on 2020-05-14 09:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('lawyers', '0012_auto_20200422_2333'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('date_added', models.DateField()),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('shelf_number', models.CharField(max_length=250)),
                ('requested', models.BooleanField(default=False)),
                ('available', models.BooleanField(default=True)),
                ('added_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='lawyers.OtherStaff')),
            ],
        ),
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='BookHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_requested', models.DateField()),
                ('returned', models.BooleanField(default=False)),
                ('approved', models.BooleanField(default=False)),
                ('date_approved', models.DateField(null=True)),
                ('date_returned', models.DateField(blank=True, null=True)),
                ('approved_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='lawyers.OtherStaff')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resources.Book')),
                ('lawyer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='lawyers.Lawyer')),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='branch',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='resources.Branch'),
        ),
        migrations.AddField(
            model_name='book',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='resources.Category'),
        ),
    ]
