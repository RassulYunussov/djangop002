# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-08 11:35
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0022_auto_20171005_1849'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='classmate',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='facebook',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='instagram',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='phone',
            field=models.CharField(blank=True, default='', max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='register_date',
            field=models.DateTimeField(default=datetime.datetime(2017, 10, 8, 11, 35, 48, 114908, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='profile',
            name='telegram_name',
            field=models.CharField(blank=True, default='', max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='twitter',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='vk',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='youtube',
            field=models.TextField(blank=True, default='', null=True),
        ),
    ]
