# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-27 08:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0012_auto_20170927_1325'),
    ]

    operations = [
        migrations.AddField(
            model_name='vilavifetch',
            name='ur',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AlterField(
            model_name='vilavifetch',
            name='q',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='vilavifetch',
            name='r',
            field=models.CharField(max_length=30),
        ),
    ]