# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-16 04:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_auto_20180515_1525'),
    ]

    operations = [
        migrations.AddField(
            model_name='repair',
            name='vehicle',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='accounts.Vehicle'),
            preserve_default=False,
        ),
    ]
