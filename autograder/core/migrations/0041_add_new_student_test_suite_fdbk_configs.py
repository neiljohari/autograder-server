# Generated by Django 2.0.1 on 2019-05-23 17:28

import autograder.core.fields
import autograder.core.models.student_test_suite.student_test_suite
from django.db import migrations


def migrate_student_test_suite_fdbk_configs(apps, schema_editor):
    StudentTestSuite = apps.get_model('core', 'StudentTestSuite')

    fdbk_field_names = [
        'normal_fdbk_config',
        'ultimate_submission_fdbk_config',
        'past_limit_submission_fdbk_config',
        'staff_viewer_fdbk_config',
    ]

    for student_suite in StudentTestSuite.objects.all():
        for field_name in fdbk_field_names:
            old_field_name = 'old_' + field_name
            fdbk = {
                'visible': getattr(student_suite, old_field_name).visible,

                'show_setup_return_code': (
                    getattr(student_suite, old_field_name).show_setup_return_code),
                'show_setup_stdout': getattr(student_suite, old_field_name).show_setup_stdout,
                'show_setup_stderr': getattr(student_suite, old_field_name).show_setup_stderr,

                'show_get_test_names_return_code': (
                    getattr(student_suite, old_field_name).show_get_test_names_return_code),
                'show_get_test_names_stdout': (
                    getattr(student_suite, old_field_name).show_get_test_names_stdout),
                'show_get_test_names_stderr': (
                    getattr(student_suite, old_field_name).show_get_test_names_stderr),

                'show_validity_check_stdout': (
                    getattr(student_suite, old_field_name).show_validity_check_stdout),
                'show_validity_check_stderr': (
                    getattr(student_suite, old_field_name).show_validity_check_stderr),

                'show_grade_buggy_impls_stdout': (
                    getattr(student_suite, old_field_name).show_grade_buggy_impls_stdout),
                'show_grade_buggy_impls_stderr': (
                    getattr(student_suite, old_field_name).show_grade_buggy_impls_stderr),

                'show_invalid_test_names': (
                    getattr(student_suite, old_field_name).show_invalid_test_names),
                'show_points': getattr(student_suite, old_field_name).show_points,
                'bugs_exposed_fdbk_level': (
                    getattr(student_suite, old_field_name).bugs_exposed_fdbk_level),
            }
            setattr(student_suite, field_name, fdbk)

        student_suite.full_clean()
        student_suite.save()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0040_rename_old_student_test_suite_fdbk_configs'),
    ]

    operations = [
        migrations.AddField(
            model_name='studenttestsuite',
            name='normal_fdbk_config',
            field=autograder.core.fields.ValidatedJSONField(default=autograder.core.models.student_test_suite.student_test_suite.NewStudentTestSuiteFeedbackConfig, help_text='Feedback settings for a normal Submission.', serializable_class=autograder.core.models.student_test_suite.student_test_suite.NewStudentTestSuiteFeedbackConfig),
        ),
        migrations.AddField(
            model_name='studenttestsuite',
            name='past_limit_submission_fdbk_config',
            field=autograder.core.fields.ValidatedJSONField(default=autograder.core.models.student_test_suite.student_test_suite.NewStudentTestSuiteFeedbackConfig.default_past_limit_submission_fdbk_config, help_text='Feedback settings for a Submission that is past the daily limit.', serializable_class=autograder.core.models.student_test_suite.student_test_suite.NewStudentTestSuiteFeedbackConfig),
        ),
        migrations.AddField(
            model_name='studenttestsuite',
            name='staff_viewer_fdbk_config',
            field=autograder.core.fields.ValidatedJSONField(default=autograder.core.models.student_test_suite.student_test_suite.NewStudentTestSuiteFeedbackConfig.max_fdbk_config, help_text='Feedback settings for a staff member viewing a Submission from another group.', serializable_class=autograder.core.models.student_test_suite.student_test_suite.NewStudentTestSuiteFeedbackConfig),
        ),
        migrations.AddField(
            model_name='studenttestsuite',
            name='ultimate_submission_fdbk_config',
            field=autograder.core.fields.ValidatedJSONField(default=autograder.core.models.student_test_suite.student_test_suite.NewStudentTestSuiteFeedbackConfig.default_ultimate_submission_fdbk_config, help_text='Feedback settings for an ultimate Submission.', serializable_class=autograder.core.models.student_test_suite.student_test_suite.NewStudentTestSuiteFeedbackConfig),
        ),

        migrations.RunPython(
            migrate_student_test_suite_fdbk_configs, lambda apps, schema_editor: None
        )
    ]