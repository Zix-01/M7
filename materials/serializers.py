from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from materials.models import Course, Lesson, Subscription
from materials.validators import YouTubeValidator


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'name', 'video_url']
        validators = [YouTubeValidator()]


class CourseSerializer(ModelSerializer):
    is_subscribed = SerializerMethodField()

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user

        if not user.is_authenticated:
            return False

        return Subscription.objects.filter(user=user, course=obj).exists()

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
