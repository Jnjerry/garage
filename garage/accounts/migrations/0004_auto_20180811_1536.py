# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-11 12:36
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_remove_repair_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Passenger',
        ),
        migrations.DeleteModel(
            name='Price',
        ),
    ]
