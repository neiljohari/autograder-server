# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-05-05 19:26
from __future__ import unicode_literals

import autograder.core.fields
import autograder.core.models.ag_model_base
import autograder.core.models.ag_test.ag_test_suite
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20170403_0213'),
    ]

    operations = [
        migrations.CreateModel(
            name='AGTestSuite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', autograder.core.fields.ShortStringField(help_text='The name used to identify this suite.\n                     Must be non-empty and non-null.\n                     Must be unique among suites that belong to the same project.\n                     This field is REQUIRED.', max_length=255, strip=False)),
                ('docker_image_to_use', autograder.core.fields.ShortStringField(choices=[('jameslp/autograder-sandbox', 'jameslp/autograder-sandbox')], default='jameslp/autograder-sandbox', help_text='The name of the Docker image that the sandbox should be created using.', max_length=255, strip=False)),
                ('allow_network_access', models.BooleanField(default=False, help_text='Specifies whether the sandbox should allow commands run inside of it to\n                     make network calls outside of the sandbox.')),
                ('deferred', models.BooleanField(default=False, help_text='If true, this test suite can be graded asynchronously. Deferred suites that\n                     have yet to be graded do not prevent members of a group from submitting\n                     again.')),
            ],
            bases=(autograder.core.models.ag_model_base._AutograderModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='AGTestSuiteFeedbackConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('show_individual_tests', models.BooleanField(default=True, help_text='Whether to show information about individual tests in a suite or just a\n                     points summary (if available).')),
                ('show_setup_command', models.BooleanField(default=True, help_text="Whether to show information about a suite's setup command.")),
            ],
            options={
                'abstract': False,
            },
            bases=(autograder.core.models.ag_model_base._AutograderModelMixin, models.Model),
        ),
        migrations.AlterField(
            model_name='autogradertestcasebase',
            name='expected_standard_error_output',
            field=models.TextField(blank=True, help_text='A string whose contents should be compared to the\n            standard error output of the program being tested. A value\n            of the empty string indicates that this test case should not\n            check the standard error output of the program being\n            tested.', validators=[django.core.validators.MaxLengthValidator(8000000)]),
        ),
        migrations.AlterField(
            model_name='autogradertestcasebase',
            name='expected_standard_output',
            field=models.TextField(blank=True, help_text='A string whose contents should be compared to the\n            standard output of the program being tested. A value of the\n            empty string indicates that this test case should not check\n            the standard output of the program being tested.', validators=[django.core.validators.MaxLengthValidator(8000000)]),
        ),
        migrations.AddField(
            model_name='agtestsuite',
            name='normal_fdbk_config',
            field=models.OneToOneField(default=autograder.core.models.ag_test.ag_test_suite.make_default_suite_fdbk, help_text='Feedback settings for a normal submission.', on_delete=django.db.models.deletion.CASCADE, related_name='+', to='core.AGTestSuiteFeedbackConfig'),
        ),
        migrations.AddField(
            model_name='agtestsuite',
            name='past_limit_submission_fdbk_config',
            field=models.OneToOneField(default=autograder.core.models.ag_test.ag_test_suite.make_default_suite_fdbk, help_text='Feedback settings for a submission that is past the daily limit.', on_delete=django.db.models.deletion.CASCADE, related_name='+', to='core.AGTestSuiteFeedbackConfig'),
        ),
        migrations.AddField(
            model_name='agtestsuite',
            name='project',
            field=models.ForeignKey(help_text='The project this suite belongs to.\n                                             This field is sREQUIRED.', on_delete=django.db.models.deletion.CASCADE, related_name='ag_test_suites', to='core.Project'),
        ),
        migrations.AddField(
            model_name='agtestsuite',
            name='project_files_needed',
            field=models.ManyToManyField(help_text="The project files that will be copied into the sandbox before the suite's\n                     tests are run.", to='core.UploadedFile'),
        ),
        migrations.AddField(
            model_name='agtestsuite',
            name='staff_viewer_fdbk_config',
            field=models.OneToOneField(default=autograder.core.models.ag_test.ag_test_suite.make_default_suite_fdbk, help_text='Feedback settings for a staff member viewing a submission from another\n                     group.', on_delete=django.db.models.deletion.CASCADE, related_name='+', to='core.AGTestSuiteFeedbackConfig'),
        ),
        migrations.AddField(
            model_name='agtestsuite',
            name='student_files_needed',
            field=models.ManyToManyField(help_text="Student-submitted files matching these patterns will be copied into the\n                     sandbox before the suite's tests are run.", to='core.ExpectedStudentFilePattern'),
        ),
        migrations.AddField(
            model_name='agtestsuite',
            name='ultimate_submission_fdbk_config',
            field=models.OneToOneField(default=autograder.core.models.ag_test.ag_test_suite.make_default_suite_fdbk, help_text='Feedback settings for an ultimate submission.', on_delete=django.db.models.deletion.CASCADE, related_name='+', to='core.AGTestSuiteFeedbackConfig'),
        ),
        migrations.AlterUniqueTogether(
            name='agtestsuite',
            unique_together=set([('name', 'project')]),
        ),
        migrations.AlterOrderWithRespectTo(
            name='agtestsuite',
            order_with_respect_to='project',
        ),
    ]