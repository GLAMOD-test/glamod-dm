# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-01-16 16:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deliveries_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stationconfigurationlookupfields',
            name='region',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
