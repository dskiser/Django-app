# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-24 19:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budget_keepers', '0018_remove_expense_note'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='red_or_black',
            field=models.CharField(default='black', max_length=5),
        ),
    ]
