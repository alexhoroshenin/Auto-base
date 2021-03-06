# Generated by Django 3.0.5 on 2020-06-09 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Auto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('car_number', models.CharField(blank=True, max_length=50, null=True)),
                ('vin_code', models.CharField(max_length=50)),
                ('color', models.CharField(blank=True, max_length=50, null=True)),
                ('mark', models.CharField(blank=True, max_length=50, null=True)),
                ('year_of_issue', models.PositiveIntegerField(blank=True, null=True)),
                ('creating_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
