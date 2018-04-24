# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-23 06:14
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20180423_0902'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mechprofile',
            name='name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mechprofile', to=settings.AUTH_USER_MODEL),
        ),
    ]