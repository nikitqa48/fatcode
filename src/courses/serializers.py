from rest_framework import serializers

from . import models
from .validators import StudentWorkValidator
from .services import test_service

from src.profiles.models import FatUser


class CodeQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CodeQuestion
        fields = ('code', 'answer')
        read_only_fields = ('code', 'answer')


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Quiz
        fields = ('text', 'lesson')
        read_only_fields = ('right', 'hint')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        fields = ('name',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ('name', 'parent')
        ref_name = 'courses_category'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = FatUser
        fields = (
            'socials',
            'first_name',
            'last_name',
            'avatar',
        )
        ref_name = 'userCourse'


class LessonDetailSerializer(serializers.ModelSerializer):
    """Урок"""
    code = CodeQuestionSerializer(many=True)
    quiz = QuizSerializer(many=True)
    work = serializers.SerializerMethodField()

    class Meta:
        model = models.Lesson
        fields = (
            'id',
            'lesson_type',
            'name',
            'viewed',
            'video_url',
            'published',
            'slug',
            'description',
            'code',
            'quiz',
            'work'
        )

    def get_work(self, instance):
        user = self.context['request'].user
        work = models.StudentWork.objects.filter(student=user, lesson=instance).first()
        serialize_work = StudentWorkSerializer(work)
        return serialize_work.data


class LessonListSerializer(serializers.ModelSerializer):
    """Список уроков"""

    class Meta:
        model = models.Lesson
        fields = (
            'id',
            'lesson_type',
            'name',
            'viewed',
            'video_url',
            'published',
            'slug',
            'description',
            'hint'
        )


class CourseSerializer(serializers.ModelSerializer):
    """Курс"""
    mentor = UserSerializer()
    author = UserSerializer()
    tags = TagSerializer(many=True)
    category = CategorySerializer()
    lessons = LessonListSerializer(many=True, required=False)

    class Meta:
        model = models.Course
        fields = (
            'id',
            'name',
            'description',
            'slug',
            'view_count',
            'published',
            'updated',
            'mentor',
            'author',
            'tags',
            'category',
            'lessons',
        )


class ListCourseSerializer(serializers.ModelSerializer):
    """Список курсов"""
    author = UserSerializer()
    tags = TagSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = models.Course
        fields = (
            'id',
            'author',
            'tags',
            'category',
            'name',
            'description',
            'published',
            'updated',
            'slug',
            'view_count'
        )


class StudentWorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StudentWork
        fields = ('lesson', 'code_answer', 'quiz_answer', 'completed', 'error')

    def validate(self, data):
        validate_class = StudentWorkValidator()
        validate_class(data)
        return data

    def create(self, validated_data):
        work = models.StudentWork.objects.create(**validated_data, student=self.context['request'].user)
        file = work.create_testfile()
        test_service.request(file, validated_data['lesson'].course.name)
        if test_service.status_code == 200:
            if 'test_django exited with code 0' in test_service.content['result']['stdout']:
                work.completed = True
                return work
            work.error = test_service.content['result']['stdout']
        return work


class HelpUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.HelpUser
        fields = ('lesson',)

    def create(self, validated_data):
        mentor = validated_data['lesson'].course.mentor
        student = self.context['request'].user
        return models.HelpUser.objects.create(mentor=mentor, student=student, **validated_data)


class PartCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PartCourse
        fields = (
            'name',
            'description',
            'position',
            'instructor',
        )


class AdminCreateCourseSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False)
    part = PartCourseSerializer(many=True, required=False)

    class Meta:
        model = models.Course
        fields = (
            'id',
            'name',
            'description',
            'slug',
            'view_count',
            'published',
            'updated',
            'mentor',
            'author',
            'tags',
            'category',
            'part'
        )

    def create(self, validated_data):
        nested_data = {'part', 'tags'}
        data = {x: validated_data[x] for x in validated_data if x not in nested_data}
        instance = models.Course.objects.create(**data)
        if 'part' in validated_data:
            x = {instance.part.create(**part) for part in validated_data.pop('part')}
        if 'tags' in validated_data:
            x = {instance.tags.create(**tag) for tag in validated_data.pop('tags')}
        return instance

