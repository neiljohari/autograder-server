# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autograder.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('autograder', '0035_auto_20151203_0114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studenttestsuitebase',
            name='compiler_flags',
            field=autograder.models.fields.StringListField(blank=True, base_field=models.CharField(blank=True, max_length=255), size=None, default=list),
        ),
    ]
