from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from courses.api.serializers import SubjectSerializer, CourseSerializer
from courses.models import Subject, Course


class SubjectListView(generics.ListAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class SubjectDetailView(generics.RetrieveAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

# replaced by @action enroll
# class CourseEnrollView(APIView):
#     """
#     APIview - only post method allowed, pk of course to indentify course
#     and add current user to it.
#     """
#     authentication_classes = (BasicAuthentication,)
#     permission_classes = (IsAuthenticated,)
#
#     def post(self, request, pk, format=None):
#         course = get_object_or_404(Course, pk=pk)
#         course.students.add(request.user)
#         return Response({'enrolled': True})

class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    @action(detail=True,
            methods=['post'],
            authentication_classes=[BasicAuthentication],
            permission_classes=[IsAuthenticated])
    def enroll(self, request, *args,**kwargs):
        """
        Custom method enables to enroll students for courses, detail=True
        specifies that action is taken on single obj (e.g.course), for method
        'post' with auth/perms specified perform enroll func: get current course
        enroll current user to it.
        """
        course = self.get_object()
        course.students.add(request.user)
        return Response({'enrolled': True})
