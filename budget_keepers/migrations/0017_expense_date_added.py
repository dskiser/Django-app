# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-24 15:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('budget_keepers', '0016_auto_20170523_1555'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
