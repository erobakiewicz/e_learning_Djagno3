from rest_framework.permissions import BasePermission


class IsEnrolled(BasePermission):
    """
    Checks if student is enrolled for course.
    """
    def has_object_permission(self, request, view, obj):
        return obj.students.filter(id=request.user.id).exists()