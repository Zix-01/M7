from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.viewsets import ModelViewSet

from materials.models import Course, Lesson, Subscription
from materials.paginators import CustomPagination
from materials.serializers import CourseSerializer, LessonSerializer
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
        return Lesson.objects.filter(owner=self.request.user)  # Фильтрация по владельцу


class SubscriptionView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get('course_id')
        course_item = get_object_or_404(Course, id=course_id)

        # Проверяем наличие подписки
        subs_item = Subscription.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            # Если подписка существует, удаляем ее
            subs_item.delete()
            message = 'Подписка удалена'
        else:
            # Если подписки нет, создаем ее
            Subscription.objects.create(user=user, course=course_item)
            message = 'Подписка добавлена'

        return Response({"message": message}, status=status.HTTP_200_OK)
