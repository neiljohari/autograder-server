from django.contrib.auth.models import User

from rest_framework import (
    viewsets, mixins, permissions, response,
    status, exceptions)

import autograder.rest_api.serializers as ag_serializers
import autograder.core.models as ag_models


class IsAdminOrReadOnlyStaff(permissions.BasePermission):
    def has_object_permission(self, request, view, course):
        is_admin = course.is_administrator(request.user)
        staff_and_read_only = (course.is_course_staff(request.user) and
                               request.method in permissions.SAFE_METHODS)
        return is_admin or staff_and_read_only


class CourseStaffViewSet(mixins.ListModelMixin,
                         viewsets.GenericViewSet):
    serializer_class = ag_serializers.UserSerializer
    permission_classes = (permissions.IsAuthenticated,
                          IsAdminOrReadOnlyStaff)

    def get_object(self, pk):
        course = ag_models.Course.objects.get(pk=pk)
        self.check_object_permissions(self.request, course)
        return course

    def get_queryset(self):
        course = self.get_object(self.kwargs['course_pk'])
        return course.staff.all()

    def post(self, request, course_pk):
        staff_to_add = [
            User.objects.get_or_create(username=username)[0]
            for username in request.data.getlist('new_staff')]
        self.get_object(course_pk).staff.add(*staff_to_add)
        return response.Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, course_pk):
        staff_to_remove = [
            User.objects.get_or_create(username=username)[0]
            for username in request.data.getlist('remove_staff')]
        self.get_object(course_pk).staff.remove(*staff_to_remove)
        return response.Response(status=status.HTTP_204_NO_CONTENT)
