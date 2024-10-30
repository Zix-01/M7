from django.urls import path
from rest_framework.routers import SimpleRouter

from materials.apps import MaterialsConfig
from materials.views import CourseViewSet, LessonListAPIView, LessonRetrieveAPIView, LessonDestroyAPIView, \
    LessonUpdateAPIView, LessonCreateApiView

app_name = MaterialsConfig.name

router = SimpleRouter()
router.register("", CourseViewSet)


urlpatterns = [
    path('materials/', LessonListAPIView.as_view(), name='materials_list'),
    path('materials/<int:pk>/', LessonRetrieveAPIView.as_view(), name='materials_retrieve'),
    path('materials/<int:pk>/update/', LessonUpdateAPIView.as_view(), name='materials_update'),
    path('materials/create/', LessonCreateApiView.as_view(), name='materials_create'),
    path('materials/<int:pk>/destroy/', LessonDestroyAPIView.as_view(), name='materials_destroy'),
]

urlpatterns += router.urls
