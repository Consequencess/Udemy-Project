from django.db.models import Avg
from rest_framework import serializers
from applications.course.models import Course, CourseItem, CourseItemFile, Files


class CourseItemFileSerializer(serializers.ModelSerializer):
    file_type = serializers.CharField(write_only=True)
    file = serializers.FileField(write_only=True, allow_null=True)
    content = serializers.CharField(write_only=True, allow_blank=True)

    class Meta:
        model = CourseItemFile
        fields = ('file_type', 'file', 'content')

    def create(self, validated_data):
        file_type = validated_data.pop('file_type')
        validated_data.pop('content', None)

        if file_type == 'article':
            validated_data.pop('file', None)

        file = validated_data.pop('file', None)

        instance = CourseItemFile.objects.create(**validated_data)

        if file_type == 'video':
            Files.objects.create(course_item_file=instance, file=file)
        elif file_type == 'slides':
            # загрузка слайдов
            pass

        return instance


class CourseItemSerializer(serializers.ModelSerializer):
    files = CourseItemFileSerializer(many=True, required=True)

    class Meta:
        model = CourseItem
        fields = ('id', 'title', 'description', 'files')

    def create(self, validated_data):
        files_data = validated_data.pop('files')
        course_item = CourseItem.objects.create(**validated_data)
        for file_data in files_data:
            file_serializer = CourseItemFileSerializer(data=file_data)
            if file_serializer.is_valid():
                file_serializer.save(course_item=course_item)
            else:
                raise serializers.ValidationError(file_serializer.errors)
        return course_item


class CoursesSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = Course
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['ratings'] = instance.ratings.all().aggregate(Avg('rating'))['rating__avg']
        rep['teacher'] = instance.user.first_name
        rep['category'] = instance.category.title
        rep['theme'] = instance.theme.title
        return rep

