# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-14 22:49
from __future__ import unicode_literals

import autograder.utilities.fields
import django.core.validators
from django.db import migrations
import re


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20160112_0437'),
    ]

    operations = [
        migrations.AlterField(
            model_name='autogradertestcasebase',
            name='command_line_arguments',
            field=autograder.utilities.fields.StringArrayField(allow_empty_strings=False, blank=True, default=list, max_string_length=255, size=None, string_validators=[django.core.validators.RegexValidator(re.compile('^[a-zA-Z0-9-_=.+]+$', 32))], strip_strings=True),
        ),
        migrations.AlterField(
            model_name='autogradertestcasebase',
            name='valgrind_flags',
            field=autograder.utilities.fields.StringArrayField(allow_empty_strings=False, blank=True, default=None, max_string_length=255, null=True, size=None, string_validators=[django.core.validators.RegexValidator(re.compile('^[a-zA-Z0-9-_=.+]+$', 32))], strip_strings=True),
        ),
        migrations.AlterField(
            model_name='compilationonlyautogradertestcase',
            name='compiler_flags',
            field=autograder.utilities.fields.StringArrayField(allow_empty_strings=False, blank=True, default=list, max_string_length=255, size=None, string_validators=[django.core.validators.RegexValidator(re.compile('^[a-zA-Z0-9-_=.+]+$', 32))], strip_strings=True),
        ),
        migrations.AlterField(
            model_name='compiledandrunautogradertestcase',
            name='compiler_flags',
            field=autograder.utilities.fields.StringArrayField(allow_empty_strings=False, blank=True, default=list, max_string_length=255, size=None, string_validators=[django.core.validators.RegexValidator(re.compile('^[a-zA-Z0-9-_=.+]+$', 32))], strip_strings=True),
        ),
        migrations.AlterField(
            model_name='compiledstudenttestsuite',
            name='compiler_flags',
            field=autograder.utilities.fields.StringArrayField(allow_empty_strings=False, blank=True, default=list, max_string_length=255, size=None, string_validators=[django.core.validators.RegexValidator(re.compile('^[a-zA-Z0-9-_=.+]+$', 32))], strip_strings=True),
        ),
        migrations.AlterField(
            model_name='interpretedautogradertestcase',
            name='interpreter_flags',
            field=autograder.utilities.fields.StringArrayField(allow_empty_strings=False, blank=True, default=list, max_string_length=255, size=None, string_validators=[django.core.validators.RegexValidator(re.compile('^[a-zA-Z0-9-_=.+]+$', 32))], strip_strings=True),
        ),
    ]