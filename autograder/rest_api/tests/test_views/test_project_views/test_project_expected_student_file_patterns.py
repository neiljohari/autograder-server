import random

from django.core.urlresolvers import reverse

from rest_framework import status

import autograder.core.models as ag_models
import autograder.rest_api.serializers as ag_serializers

from autograder.core.tests.temporary_filesystem_test_case import (
    TemporaryFilesystemTestCase)
import autograder.rest_api.tests.test_views.common_generic_data as test_data


class _PatternSetUp(test_data.Client, test_data.Project):
    pass
    # def setUp(self):
    #     super().setUp()
    #     self.url = reverse('project-patterns-list', kwargs={'pk': self.project.pk})


class ListPatternsTestCase(_PatternSetUp, TemporaryFilesystemTestCase):
    def test_admin_list_patterns(self):
        for project in self.all_projects:
            self.do_list_patterns_test(self.admin, project)

    def test_staff_list_patterns(self):
        for project in self.all_projects:
            self.do_list_patterns_test(self.staff, project)

    def test_enrolled_list_patterns(self):
        for project in self.visible_projects:
            self.do_list_patterns_test(self.enrolled, project)

        for project in self.hidden_projects:
            self.do_permission_denied_test(self.enrolled, project)

    def test_other_list_patterns(self):
        self.do_list_patterns_test(self.nobody, self.visible_public_project)

        for project in [self.visible_private_project] + self.hidden_projects:
            self.do_permission_denied_test(self.nobody, project)

    def do_list_patterns_test(self, user, project):
        serialized_patterns = self.build_patterns(project)
        self.client.force_authenticate(user)
        response = self.client.get(self.get_patterns_url(project))
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertCountEqual(serialized_patterns, response.data)

    def do_permission_denied_test(self, user, project):
        self.build_patterns(project)
        self.client.force_authenticate(user)
        response = self.client.get(self.get_patterns_url(project))
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def build_patterns(self, project):
        num_patterns = 4
        if not project.expected_student_file_patterns.count():
            for i in range(num_patterns):
                min_matches = random.randint(0, 3)
                max_matches = min_matches + 2
                ag_models.ExpectedStudentFilePattern.objects.validate_and_create(
                    project=project,
                    pattern=project.name + '_pattern_' + str(i),
                    min_num_matches=min_matches,
                    max_num_matches=max_matches)

        serialized_patterns = (
            ag_serializers.ExpectedStudentFilePatternSerializer(
                project.expected_student_file_patterns.all(), many=True)
        ).data
        self.assertEqual(num_patterns, len(serialized_patterns))
        return serialized_patterns


class CreatePatternTestCase(_PatternSetUp, TemporaryFilesystemTestCase):
    def test_admin_create_pattern(self):
        self.fail()

    def test_admin_create_pattern_invalid_settings(self):
        self.fail()

    def test_other_create_pattern_permission_denied(self):
        self.fail()