# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-11-02 21:46
from __future__ import unicode_literals

import autograder.core.models.ag_model_base
from django.conf import settings
import django.contrib.postgres.fields
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0011_auto_20171016_0422'),
    ]

    operations = [
        migrations.CreateModel(
            name='RerunSubmissionsTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('error_msg', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('rerun_all_submissions', models.BooleanField(default=True, help_text='When True, indicates that all submissions for the specified\n                     project should be rerun. Otherwise, only the submissions\n                     whose primary keys are listed in submission_pks should be rerun.')),
                ('submission_pks', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), blank=True, default=list, help_text='When rerun_all_submissions is False, specifies which submissions\n                     should be rerun.', size=None)),
                ('rerun_all_ag_test_suites', models.BooleanField(default=True, help_text='When True, indicates that all AGTestSuites belonging\n                     to the specified project should be rerun. Otherwise,\n                     only the AGTestSuites specified in ag_test_suite_data should\n                     be rerun.')),
                ('ag_test_suite_data', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, help_text='When rerun_all_ag_test_suites is False, specifies which\n                     AGTestSuites should be rerun and which AGTestCases within\n                     those suites should be rerun.\n        Data format:\n        {\n            // Note: JSON format requires that keys are strings. Postgres\n            // doesn\'t seem to care, but some JSON serializers might.\n            "<ag_test_suite_pk>": [<ag_test_case_pk>, ...],\n            ...\n        }\n        If an ag_test_suite_pk is mapped to an empty list, then all ag test cases\n        belonging to that ag test suite will be rerun.')),
                ('rerun_all_student_test_suites', models.BooleanField(default=True, help_text='When True, indicates that all StudentTestSuites belonging\n                     to the specified project should be rerun. Otherwise,\n                     only the StudentTestSuites specified in student_test_suite_pks\n                     should be rerun.')),
                ('student_suite_pks', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), blank=True, default=list, help_text='When rerun_all_student_test_suites is False, specifies which\n                     student test suites should be rerun.', size=None)),
                ('num_completed_subtasks', models.IntegerField(default=0)),
                ('celery_group_result_id', models.UUIDField(blank=True, default=None, null=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(help_text='The Project this task belongs to.', on_delete=django.db.models.deletion.CASCADE, related_name='rerun_submission_tasks', to='core.Project')),
            ],
            options={
                'abstract': False,
            },
            bases=(autograder.core.models.ag_model_base.ToDictMixin, models.Model),
        ),
    ]