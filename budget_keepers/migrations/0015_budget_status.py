# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-22 19:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budget_keepers', '0014_budget_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='budget',
            name='status',
            field=models.CharField(choices=[('active', 'active'), ('inactive', 'inactive')], default='inactive', max_length=8),
        ),
    ]
