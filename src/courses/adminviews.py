from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import CreateAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.views import APIView

from . import serializers, models
from .filters import CourseFilter
from .services import git_service

from ..base import classes


class AdminCourseView(classes.MixedPermissionSerializer, ModelViewSet):
    filter_backends = [DjangoFilterBackend]
    filterset_class = CourseFilter
    serializer_classes_by_action = {
        "create": serializers.AdminCreateCourseSerializer,
        "update": serializers.CourseSerializer,
        "destroy": serializers.CourseSerializer,
        "retrieve": serializers.CourseSerializer,
    }
    permission_classes_by_action = {
        "create": (IsAdminUser,),
        "update": (IsAdminUser,),
        "destroy": (IsAdminUser,),
        "retrieve": (IsAuthenticated,)
    }

    def get_queryset(self):
        return (
            models.Course.objects
                .select_related('author', 'category', 'mentor')
                .prefetch_related('students', 'tags')
                .all()
        )


class LessonView(classes.MixedPermissionSerializer, ModelViewSet):
    queryset = models.Lesson.objects.select_related('course').all()
    serializer_classes_by_action = {
        "create": serializers.LessonDetailSerializer,
        "update": serializers.LessonDetailSerializer,
        "destroy": serializers.LessonDetailSerializer,
        "list": serializers.LessonListSerializer,
        "retrieve": serializers.LessonDetailSerializer,
    }
    permission_classes_by_action = {
        "create": (IsAdminUser,),
        "update": (IsAdminUser,),
        "destroy": (IsAdminUser,),
        "retrieve": (IsAuthenticated,),
        "list": (AllowAny,)
    }


class RepositoryView(classes.MixedPermission, APIView):
    permission_classes_by_action = {
        "create": (IsAdminUser,),
        "list": (IsAdminUser,)
    }


class StudentWorkView(CreateAPIView):
    queryset = models.StudentWork.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.StudentWorkSerializer


class HelpUserView(CreateAPIView):
    queryset = models.HelpUser
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.HelpUserSerializer

