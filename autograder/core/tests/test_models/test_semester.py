import os

from django.core.exceptions import ValidationError

from autograder.core.models import Semester, Course

import autograder.core.shared.utilities as ut

from autograder.core.tests.temporary_filesystem_test_case import (
    TemporaryFilesystemTestCase)

import autograder.core.tests.dummy_object_utils as obj_ut


class SemesterTestCase(TemporaryFilesystemTestCase):
    def setUp(self):
        super().setUp()
        self.course = Course.objects.validate_and_create(name="eecs280")
        self.SEMESTER_NAME = "fall2015"

    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------

    def test_valid_initialization(self):
        new_semester = Semester.objects.validate_and_create(
            name=self.SEMESTER_NAME, course=self.course)

        loaded_semester = Semester.objects.get(
            name=self.SEMESTER_NAME, course=self.course)
        self.assertEqual(loaded_semester.name, self.SEMESTER_NAME)
        self.assertEqual(loaded_semester.course, self.course)
        self.assertEqual(new_semester, loaded_semester)

    def test_name_whitespace_stripped(self):
        Semester.objects.validate_and_create(
            name='    ' + self.SEMESTER_NAME + '   ',
            course=self.course)

        loaded_semester = Semester.objects.get(
            name=self.SEMESTER_NAME, course=self.course)
        self.assertEqual(loaded_semester.name, self.SEMESTER_NAME)

    def test_exception_on_name_is_only_whitespace(self):
        with self.assertRaises(ValidationError) as cm:
            Semester.objects.validate_and_create(
                name='    ', course=self.course)
        self.assertTrue('name' in cm.exception.message_dict)

    def test_exception_on_empty_name(self):
        with self.assertRaises(ValidationError) as cm:
            Semester.objects.validate_and_create(name='', course=self.course)
        self.assertTrue('name' in cm.exception.message_dict)

    def test_exception_on_null_name(self):
        with self.assertRaises(ValidationError) as cm:
            Semester.objects.validate_and_create(name=None, course=self.course)
        self.assertTrue('name' in cm.exception.message_dict)

    def test_exception_on_non_unique_name(self):
        Semester.objects.validate_and_create(
            name=self.SEMESTER_NAME, course=self.course)

        with self.assertRaises(ValidationError):
            Semester.objects.validate_and_create(
                name=self.SEMESTER_NAME, course=self.course)

    def test_no_exception_same_name_different_course(self):
        new_course_name = "eecs381"
        new_course = Course(name=new_course_name)
        new_course.validate_and_save()

        Semester.objects.validate_and_create(
            name=self.SEMESTER_NAME, course=self.course)

        new_semester = Semester.objects.validate_and_create(
            name=self.SEMESTER_NAME, course=new_course)

        loaded_new_semester = Semester.objects.get(
            name=self.SEMESTER_NAME, course=new_course)

        self.assertEqual(loaded_new_semester, new_semester)


# -----------------------------------------------------------------------------

class SemesterStaffAndEnrolledStudentTestCase(TemporaryFilesystemTestCase):
    def setUp(self):
        super().setUp()

        self.course = obj_ut.create_dummy_courses()
        self.semester = obj_ut.create_dummy_semesters(self.course)
        self.user = obj_ut.create_dummy_user()

    def test_valid_add_semester_staff(self):
        self.semester.add_semester_staff(self.user)

        loaded = Semester.objects.get(pk=self.semester.pk)
        self.assertTrue(loaded.is_semester_staff(self.user))

    def test_add_semester_staff_ignore_duplicates(self):
        self.semester.add_semester_staff(self.user)

        user2 = obj_ut.create_dummy_user()
        self.semester.add_semester_staff(self.user, user2)

        loaded = Semester.objects.get(pk=self.semester.pk)
        self.assertCountEqual(
            (self.user.username, user2.username), loaded.semester_staff_names)

    def test_valid_remove_semester_staff(self):
        self.semester.add_semester_staff(self.user)
        self.assertTrue(self.semester.is_semester_staff(self.user))

        self.semester.remove_semester_staff(self.user)
        loaded = Semester.objects.get(pk=self.semester.pk)
        self.assertFalse(loaded.is_semester_staff(self.user))

    def test_valid_remove_multiple_staff(self):
        more_users = obj_ut.create_dummy_users(3)
        self.semester.add_semester_staff(*more_users)
        self.assertCountEqual(
            self.semester.semester_staff_names,
            (user.username for user in more_users))

        self.semester.remove_semester_staff(more_users[0], more_users[2])

        loaded = Semester.objects.get(pk=self.semester.pk)
        self.assertCountEqual(
            loaded.semester_staff_names, [more_users[1].username])

    # def test_exception_remove_user_not_semester_staff(self):
    #     with self.assertRaises(ValidationError):
    #         self.semester.remove_semester_staff(self.user)

    def test_is_semester_staff(self):
        self.assertFalse(self.semester.is_semester_staff(self.user))
        # self.assertFalse(self.semester.is_semester_staff(self.user.username))

        self.semester.add_semester_staff(self.user)
        self.assertTrue(self.semester.is_semester_staff(self.user))
        # self.assertTrue(self.semester.is_semester_staff(self.user.username))

    def test_valid_add_enrolled_students(self):
        self.semester.add_enrolled_students(self.user)

        loaded = Semester.objects.get(pk=self.semester.pk)
        self.assertTrue(loaded.is_enrolled_student(self.user))

    def test_add_enrolled_students_ignore_duplicates(self):
        self.semester.add_enrolled_students(self.user)

        user2 = obj_ut.create_dummy_user()
        self.semester.add_enrolled_students(self.user, user2)

        loaded = Semester.objects.get(pk=self.semester.pk)
        self.assertCountEqual(
            (self.user.username, user2.username),
            loaded.enrolled_student_names)

    def test_valid_remove_enrolled_student(self):
        self.semester.add_enrolled_students(self.user)
        self.assertTrue(self.semester.is_enrolled_student(self.user))

        self.semester.remove_enrolled_students(self.user)

        loaded = Semester.objects.get(pk=self.semester.pk)
        self.assertFalse(loaded.is_enrolled_student(self.user))

    def test_valid_remove_multiple_students(self):
        more_users = obj_ut.create_dummy_users(3)
        self.semester.add_enrolled_students(*more_users)
        self.assertCountEqual(
            self.semester.enrolled_student_names,
            (user.username for user in more_users))

        self.semester.remove_enrolled_students(more_users[0], more_users[2])

        loaded = Semester.objects.get(pk=self.semester.pk)
        self.assertCountEqual(
            loaded.enrolled_student_names, [more_users[1].username])

    # def test_exception_on_remove_user_not_enrolled_student(self):
    #     with self.assertRaises(ValidationError):
    #         self.semester.remove_enrolled_students(self.user)

    def test_is_enrolled_student(self):
        self.assertFalse(self.semester.is_enrolled_student(self.user))
        # self.assertFalse(self.semester.is_enrolled_student(self.user.username))

        self.semester.add_enrolled_students(self.user)
        self.assertTrue(self.semester.is_enrolled_student(self.user))
        # self.assertTrue(self.semester.is_enrolled_student(self.user.username))

    def test_get_staff_semesters_for_user(self):
        # Staff only
        expected_semesters = [
            obj_ut.build_semester(semester_kwargs={'staff': [self.user]})
            for i in range(4)
        ]
        # Staff and admin
        expected_semesters.append(obj_ut.build_semester(
            course_kwargs={'administrators': [self.user]},
            semester_kwargs={'staff': [self.user]}))
        # Admin only
        expected_semesters.append(obj_ut.build_semester(
            course_kwargs={'administrators': [self.user]}))
        # Nothing
        obj_ut.build_semester()

        actual_semesters = Semester.get_staff_semesters_for_user(self.user)
        self.assertCountEqual(expected_semesters, actual_semesters)

    def test_get_enrolled_semesters_for_user(self):
        semesters = obj_ut.create_dummy_semesters(self.course, 10)
        subset = [semesters[3], semesters[8]]
        for semester in subset:
            semester.add_enrolled_students(self.user)

        semesters_queryset = Semester.get_enrolled_semesters_for_user(
            self.user)
        self.assertCountEqual(semesters_queryset, subset)

    def test_semester_staff_names_includes_administrators(self):
        self.course.add_administrators(self.user)

        self.assertTrue(self.semester.is_semester_staff(self.user))
        self.assertCountEqual(
            (self.user.username,), self.semester.semester_staff_names)


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

class SemesterFilesystemTestCase(TemporaryFilesystemTestCase):
    def setUp(self):
        super().setUp()
        self.course = Course.objects.validate_and_create(name="eecs280")
        self.SEMESTER_NAME = "fall2015"

    # -------------------------------------------------------------------------

    def test_semester_root_dir_created_and_removed(self):
        semester = Semester(name=self.SEMESTER_NAME, course=self.course)

        self.assertEqual(
            [],
            os.listdir(os.path.dirname(ut.get_semester_root_dir(semester))))

        semester.validate_and_save()

        expected_semester_root_dir = ut.get_semester_root_dir(semester)
        self.assertTrue(os.path.isdir(expected_semester_root_dir))

        semester.delete()
        self.assertFalse(os.path.exists(expected_semester_root_dir))