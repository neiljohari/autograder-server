# Generated by Django 2.0.1 on 2019-03-07 20:08

from django.db import migrations


def set_suite_sandbox_images(apps, schema_editor):
    AGTestSuite = apps.get_model('core', 'AGTestSuite')
    StudentTestSuite = apps.get_model('core', 'StudentTestSuite')
    SandboxDockerImage = apps.get_model('core', 'SandboxDockerImage')

    # In migration 0037, we created a table entry for each SupportedImage,
    # using those values as the names of the new objects.
    for ag_test_suite in AGTestSuite.objects.all():
        print(ag_test_suite.docker_image_to_use.value)
        ag_test_suite.sandbox_docker_image = SandboxDockerImage.objects.get(
            name=ag_test_suite.docker_image_to_use.value
        )
        ag_test_suite.save()

    for student_suite in StudentTestSuite.objects.all():
        print(student_suite.docker_image_to_use.value)
        student_suite.sandbox_docker_image = SandboxDockerImage.objects.get(
            name=student_suite.docker_image_to_use.value
        )
        student_suite.save()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0038_ag_test_suite_student_test_suite_sandbox_docker_image'),
    ]

    operations = [
        migrations.RunPython(set_suite_sandbox_images,
                             reverse_code=lambda apps, schema_editor: None),
    ]