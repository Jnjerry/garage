# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-27 09:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicle',
            name='car_make',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='car_model',
            field=models.CharField(max_length=255),
        ),
    ]