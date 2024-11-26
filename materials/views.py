from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.viewsets import ModelViewSet

from materials.models import Course, Lesson, Subscription
from materials.paginators import CustomPagination
from materials.serializers import CourseSerializer, LessonSerializer, SubscriptionSerializer
from users.permissions import IsModerator, IsOwner
import requests


class CourseListView(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CustomPagination
    permission_classes = (IsAuthenticated,)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class LessonCreateApiView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, ~IsModerator,)  # IsAuthenticated первым

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


class LessonListAPIView(ListAPIView):
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated,)  # Доступ к объектам только для аутентифицированных пользователей

    def get_queryset(self):
        return Lesson.objects.filter(owner=self.request.user)  # Фильтрация по владельцу


class LessonRetrieveAPIView(RetrieveAPIView):
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated,)  # Доступ только для аутентифицированных пользователей

    def get_queryset(self):
        return Lesson.objects.filter(owner=self.request.user)  # Фильтрация по владельцу


class LessonUpdateAPIView(UpdateAPIView):
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModerator | IsOwner,)  # IsAuthenticated первым

    def get_queryset(self):
        return Lesson.objects.filter(owner=self.request.user)  # Фильтрация по владельцу


class LessonDestroyAPIView(DestroyAPIView):
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, ~IsModerator | IsOwner,)  # IsAuthenticated первым

    def get_queryset(self):
        return Lesson.objects.filter(owner=self.request.user)


class SubscriptionCreateAPIView(CreateAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = self.request.user
        course_id = request.data.get('course')
        course = get_object_or_404(Course, pk=course_id)
        subs_item = Subscription.objects.filter(user=user, course=course)
        if subs_item.exists():
            subs_item.delete()
            message = 'Подписка удалена'
        else:
            Subscription.objects.create(user=user, course=course, sign_up=True)
            message = 'Подписка добавлена'
        return Response({'message': message})
