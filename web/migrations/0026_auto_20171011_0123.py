# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-10 19:23
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0025_auto_20171010_2119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='register_date',
            field=models.DateTimeField(default=datetime.datetime(2017, 10, 10, 19, 23, 4, 471650, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='vilavifetch',
            name='lastTimeShow',
            field=models.DateTimeField(default=datetime.datetime(2017, 10, 10, 19, 23, 4, 473159, tzinfo=utc)),
        ),
    ]