from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from materials.models import Course, Lesson


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class LessonAmountSerializer(ModelSerializer):
    lessons_amount = SerializerMethodField()
    lessons = LessonSerializer(many=True)

    def get_lessons_amount(self, course):
        return Lesson.objects.filter(lesson=course.lesson).count()

    class Meta:
        model = Lesson
        fields = ('name', 'description', 'lessons_amount', 'lessons')
