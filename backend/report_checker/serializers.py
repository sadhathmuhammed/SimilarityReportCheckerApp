from rest_framework import serializers
from .models import Submission, SubmissionVersion, Faculty, Student

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

class StudentRegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Student
        fields = ['username', 'password', 'name', 'email', 'faculty']

class FacultyRegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Faculty
        fields = ['username', 'password', 'name', 'email', 'department']

class SubmissionVersionSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='submission.student.name',
                                         read_only=True)
    student_id = serializers.IntegerField(source='submission.student.student_id',
                                          read_only=True)

    class Meta:
        model = SubmissionVersion
        fields = [
            'id',
            'submission',
            'version',
            'docx_file',
            'ppt_file',
            'similarity_report',
            'upload_timestamp',
            'status',
            'remarks',
            'similarity_percentage',
            'student_name',
            'student_id',
        ]


class SubmissionSerializer(serializers.ModelSerializer):
    versions = SubmissionVersionSerializer(many=True, read_only=True)

    class Meta:
        model = Submission
        fields = '__all__'

class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = ['id', 'name', 'department']

