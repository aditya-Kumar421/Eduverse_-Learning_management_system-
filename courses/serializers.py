from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Course, Comment, CourseSection, Episode, Cart
from users.serializers import UserSerializer

class CourseDisplaySerializer(ModelSerializer):
    student_no = serializers.IntegerField(source='get_enrolled_student')

    class Meta:
        model = Course
        fields = ["course_uuid", "title", "student_no", "author", "price","image_url"]
           
class CommentSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model=Comment
        exclude=[
            'id'
        ]

class EpisodeSerializer(ModelSerializer):
    length=serializers.CharField(source='get_video_length_time')
    class Meta:
        model=Episode
        fields=[
            "title",
            "length",
            "file" 
        ] 

class CourseSectionSerializer(ModelSerializer):
    episodes=EpisodeSerializer(many=True)
    total_duration=serializers.CharField(source='total_length')
    class Meta:
        model=CourseSection
        fields=[
            'section_title',
            'episodes',
            'total_duration',
        ]

class CourseSerializer(ModelSerializer):
    comments=CommentSerializer(many=True)
    course_section=CourseSectionSerializer(many=True)
    student_no=serializers.IntegerField(source='get_enrolled_student')
    total_lectures=serializers.IntegerField(source='get_total_lectures')
    total_duration=serializers.CharField(source='total_course_length')
    class Meta:
        model=Course
        exclude=[
            'id'
        ]

class CourseListSerailizer(ModelSerializer):
    student_no=serializers.IntegerField(source='get_enrolled_student')
    description=serializers.CharField(source='get_brief_description')
    total_lectures=serializers.IntegerField(source='get_total_lectures')
    class Meta:
        model=Course
        fields =[
            'course_uuid',
            'title',
            'student_no',
            'author',
            'price',
            'image_url',
            'description',
            'total_lectures'
        ]

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        exclude=['id']


