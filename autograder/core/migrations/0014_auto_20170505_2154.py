# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-05-05 21:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_auto_20170505_2153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agtestcase',
            name='ag_test_suite',
            field=models.ForeignKey(help_text='The suite this autograder test belongs to.\n                     This field is REQUIRED.', on_delete=django.db.models.deletion.CASCADE, related_name='ag_test_cases', to='core.AGTestSuite'),
        ),
    ]