from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import transaction

import autograder.core.models as ag_models

from autograder import utils


@transaction.atomic()
def copy_project(project: ag_models.Project, target_course: ag_models.Course,
                 new_project_name: str=None):
    new_project = ag_models.Project.objects.get(pk=project.pk)
    new_project.pk = None
    new_project.course = target_course
    if new_project_name is not None:
        new_project.name = new_project_name

    new_project.save()

    for uploaded_file in project.uploaded_files.all():
        with uploaded_file.open('rb') as f:
            ag_models.UploadedFile.objects.validate_and_create(
                project=new_project,
                file_obj=SimpleUploadedFile(uploaded_file.name, f.read()))

    for pattern in project.expected_student_file_patterns.all():
        pattern.pk = None
        pattern.project = new_project
        pattern.save()

    for suite in project.ag_test_suites.all():
        project_files_needed = [
            file_ for file_ in new_project.uploaded_files.all()
            if utils.find_if(suite.project_files_needed.all(),
                             lambda proj_file: proj_file.name == file_.name)
            ]
        student_files_needed = list(
            new_project.expected_student_file_patterns.filter(
                pattern__in=[pattern.pattern for pattern in suite.student_files_needed.all()]))

        new_suite = ag_models.AGTestSuite.objects.validate_and_create(
            project=new_project,
            project_files_needed=project_files_needed,
            student_files_needed=student_files_needed,
            **utils.exclude_dict(
                suite.to_dict(),
                ('pk', 'project') + ag_models.AGTestSuite.get_serialize_related_fields())
        )

        for case in suite.ag_test_cases.all():
            new_case = ag_models.AGTestCase.objects.validate_and_create(
                ag_test_suite=new_suite,
                **utils.exclude_dict(
                    case.to_dict(),
                    ('pk', 'ag_test_suite') + ag_models.AGTestCase.get_serialize_related_fields())
            )

            for cmd in case.ag_test_commands.all():
                ag_models.AGTestCommand.objects.validate_and_create(
                    ag_test_case=new_case,
                    **utils.exclude_dict(cmd.to_dict(),
                                         ('pk', 'ag_test_case') +
                                            ag_models.AGTestCommand.get_serialize_related_fields())
                )

    return new_project


@transaction.atomic()
def copy_course(course: ag_models.Course, new_course_name: str):
    new_course = ag_models.Course.objects.get(pk=course.pk)
    new_course.pk = None
    if new_course_name is not None:
        new_course.name = new_course_name

    new_course.save()

    for project in course.projects.all():
        copy_project(project, new_course)
