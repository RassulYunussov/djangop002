# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-04 12:48
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0018_auto_20171004_1845'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='register_date',
            field=models.DateTimeField(default=datetime.datetime(2017, 10, 4, 12, 48, 15, 53567, tzinfo=utc)),
        ),
    ]