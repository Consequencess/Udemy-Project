from rest_framework.permissions import BasePermission, SAFE_METHODS
from applications.course.models import Course


class IsMentorOfCourseOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if isinstance(obj, Course):
            return obj.user == request.user
        return False