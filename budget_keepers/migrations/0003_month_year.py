# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-20 15:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('budget_keepers', '0002_expense_year'),
    ]

    operations = [
        migrations.AddField(
            model_name='month',
            name='year',
            field=models.ForeignKey(default=2017, on_delete=django.db.models.deletion.CASCADE, to='budget_keepers.Year'),
            preserve_default=False,
        ),
    ]