# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-27 07:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0010_auto_20170923_0631'),
    ]

    operations = [
        migrations.AddField(
            model_name='vilavifetch',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]