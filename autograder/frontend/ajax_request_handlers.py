import os
import json
import traceback
# import datetime

from django.utils import timezone

from django.views.generic.base import View
from django.views.generic.edit import CreateView, DeleteView

from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.forms.forms import NON_FIELD_ERRORS

from django.shortcuts import get_object_or_404, render

from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden, HttpResponseNotFound

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# from django.views.decorators.csrf import ensure_csrf_cookie
# from django.utils.decorators import method_decorator
from autograder.models import Course, Semester


class ExceptionLoggingView(View):
    """
    View base class that catches any exceptions thrown from dispatch(),
    prints them to the console, and then rethrows.
    """
    def dispatch(self, *args, **kwargs):
        try:
            return super().dispatch(*args, **kwargs)
        except Exception:
            traceback.print_exc()
            raise


class LoginRequiredView(ExceptionLoggingView):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class GetCourse(LoginRequiredView):
    def get(self, request, course_id):
        try:
            course = Course.objects.get(pk=course_id)
        except ObjectDoesNotExist:
            return HttpResponseNotFound()

        if not course.is_course_admin(self.request.user):
            return HttpResponseForbidden()

        response_content = {
            'data': {
                'type': 'course',
                'id': course.pk,
                'attributes': {
                    'name': course.name,
                    'course_admin_names': course.course_admin_names
                },
                'links': {
                    'self': reverse('get-course', args=[course.pk])
                }
            },
            'included': [
                {
                    'data': {
                        'type': 'semester',
                        'id': semester.pk,
                        'links': {
                            'self': reverse('get-semester', args=[semester.pk])
                        }
                    }
                }
                for semester in course.semesters.all().order_by('pk')
            ]
        }

        return JsonResponse(response_content, safe=False)


class ListCourses(LoginRequiredView):
    """
    Reponse list content determinied by user permissions.
    """
    def get(self, request):
        courses = Course.get_courses_for_user(request.user)
        data = {
            'data': [
                {
                    'type': 'course',
                    'id': course.pk,
                    'attributes': {
                        'name': course.name,
                        'course_admin_names': course.course_admin_names
                    },
                    'links': {
                        'self': reverse('get-course', args=[course.pk])
                    }
                } for course in courses
            ]
        }

        return JsonResponse(data, safe=False)


# Move superuser things to Django Admin page
# class AddCourse(ExceptionLoggingView):
#     """
#     Permissions required: Superuser
#     """
#     pass


# class AddCourseAdmin(ExceptionLoggingView):
#     """
#     Permissions required: Superuser
#     """
#     pass


# class RemoveCourseAdmin(ExceptionLoggingView):
#     """
#     Permissions required: Superuser
#     """
#     pass


# -----------------------------------------------------------------------------

class GetSemester(LoginRequiredView):
    pass
    # def get(self, request, semester_id):
    #     pass

class ListSemesters(LoginRequiredView):
    """
    Reponse list content determinied by user permissions.
    """
    def get(self, request):
        staff_semesters = Semester.get_staff_semesters_for_user(request.user)
        enrolled_semesters = Semester.get_enrolled_semesters_for_user(
            request.user)

        data = {
            'data': [
                {
                    'type': 'semester',
                    'id': semester.pk,
                    'attributes': {
                        'name': semester.name,
                        # ('semester_staff_names': semester.semester_staff_names,
                        #  'enrolled_student_names': semester.enrolled_student_names
                        #  if semester in staff_semesters)
                    },
                    'relationships': {
                        'course': {
                            'data': {
                                'type': 'course',
                                'id': semester.course.id
                            },
                            'links': {
                                'self': reverse(
                                    'get-course', args=[semester.course.id])
                            }
                        }
                    },
                    'meta': {
                        'is_staff': (semester in staff_semesters)
                    }
                }
                for semester in sorted(list(staff_semesters.all()) + list(enrolled_semesters.all()), key=lambda obj: obj.pk)
            ]
        }

        return JsonResponse(data, safe=False)


class AddSemester(LoginRequiredView):
    """
    Permissions required: Course admin
    """
    def post(self, request):
        course = Course.objects.get(name=request.POST['course_name'])
        if not course.is_course_admin(request.user):
            return HttpResponseForbidden()

        try:
            new_semester = Semester.objects.validate_and_create(
                name=request.POST['semester_name'],
                course=course)
            return JsonResponse({
                'semester_name': new_semester.name,
                'course_name': course.name
            })
        except ValidationError as e:
            return JsonResponse({'errors': e.message_dict}, safe=False)


class ListSemesterStaff(LoginRequiredView):
    """
    Permissions required: Course admin or Semester staff
    """
    def post(self, request):
        course = Course.objects.get(name=request.POST['course_name'])
        semester = Semester.objects.get(
            name=request.POST['semester_name'], course=course)

        can_view_staff = (
            semester.is_semester_staff(request.user) or
            course.is_course_admin(request.user))
        if not can_view_staff:
            return HttpResponseForbidden()

        data = {
            'semester_name': semester.name,
            'course_name': course.name,
            'semester_staff': semester.semester_staff_names,
            'course_admins': course.course_admin_names
        }

        return JsonResponse(data, safe=False)


class AddSemesterStaff(LoginRequiredView):
    """
    Permissions required: Course admin
    """
    def post(self, request):
        pass


class RemoveSemesterStaff(LoginRequiredView):
    """
    Permissions required: Course admin
    """
    pass


class ListEnrolledStudents(LoginRequiredView):
    """
    Permissions required: Course admin or Semester staff
    """
    pass


class AddEnrolledStudents(LoginRequiredView):
    """
    Permissions required: Course admin or Semester staff
    """
    pass


class RemoveEnrolledStudents(LoginRequiredView):
    """
    Permissions required: Course admin
    """
    pass


# -----------------------------------------------------------------------------

class ProjectRequestHandler(LoginRequiredView):
    pass


class GetProjectFile(LoginRequiredView):
    pass


class ListProjects(LoginRequiredView):
    """
    Reponse list content determinied by choice of Semester
    and user permissions.
    """
    pass


class AddProject(LoginRequiredView):
    """
    Permissions required: Course admin
    """
    pass


class EditProject(LoginRequiredView):
    """
    Permissions required: Course admin
    """
    pass


class DeleteProject(LoginRequiredView):
    """
    Permissions required: Course admin
    """
    pass


class AddTestCase(LoginRequiredView):
    """
    Permissions required: Course admin
    """
    pass


class EditTestCase(LoginRequiredView):
    """
    Permissions required: Course admin
    """
    pass


class DeleteTestCase(LoginRequiredView):
    """
    Permissions required: Course admin
    """
    pass


class CopyTestCase(LoginRequiredView):
    """
    Permissions required: Course admin
    """
    pass


class CopyProjectForNewSemester(LoginRequiredView):
    """
    Permissions required: Course admin
    """
    pass


class SubmitProject(LoginRequiredView):
    """

    """
    pass


class ListSubmissions(LoginRequiredView):
    """
    Reponse list content determinied by user permissions.
    """
    pass


class ListSubmissionGroups(LoginRequiredView):
    """
    Reponse list content determinied by user permissions.
    """
    pass


class AddSubmissionGroup(LoginRequiredView):
    """
    Permissions required: Course admin
    """
    pass


class RemoveSubmissionGroup(LoginRequiredView):
    """
    Permissions required: Course admin
    """
    pass