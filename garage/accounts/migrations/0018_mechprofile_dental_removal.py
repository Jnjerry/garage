# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-18 13:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_repair_vehicle'),
    ]

    operations = [
        migrations.AddField(
            model_name='mechprofile',
            name='dental_removal',
            field=models.BooleanField(default=1),
            preserve_default=False,
        ),
    ]
