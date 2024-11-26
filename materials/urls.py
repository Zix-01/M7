from django.urls import path
from rest_framework.routers import SimpleRouter, DefaultRouter

from materials.apps import MaterialsConfig
from materials.views import LessonListAPIView, LessonRetrieveAPIView, LessonDestroyAPIView, \
    LessonUpdateAPIView, LessonCreateApiView, SubscriptionView, CourseListView

app_name = MaterialsConfig.name

router = SimpleRouter()
router.register("", CourseListView)

router = DefaultRouter()
router.register(r'courses', CourseListView, basename='course')

urlpatterns = router.urls

urlpatterns = [
    path('subscribe/', SubscriptionView.as_view(), name='subscribe'),

    path('materials/', LessonListAPIView.as_view(), name='materials_list'),
    path('materials/<int:pk>/', LessonRetrieveAPIView.as_view(), name='materials_retrieve'),
    path('materials/<int:pk>/update/', LessonUpdateAPIView.as_view(), name='materials_update'),
    path('materials/create/', LessonCreateApiView.as_view(), name='materials_create'),
    path('materials/<int:pk>/destroy/', LessonDestroyAPIView.as_view(), name='materials_destroy'),
]

urlpatterns += router.urls
