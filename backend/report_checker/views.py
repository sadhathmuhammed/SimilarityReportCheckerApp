from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status

from .models import Student, Faculty, Submission, SubmissionVersion
from report_checker.serializers import LoginSerializer, FacultySerializer
from .utils import extract_similarity_percentage
from .tasks import send_submission_email
from .serializers import SubmissionSerializer, SubmissionVersionSerializer, StudentRegisterSerializer, FacultyRegisterSerializer


class LoginView(APIView):
    """
    API endpoint for users to login.
    """
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Handle login request.
        """
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )
        if user is None:
            return Response(
                {"detail": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        else:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'username': user.username,
                'is_staff': user.is_staff
            })
        return Response({"error": "Invalid credentials"}, status=400)

class StudentUploadView(APIView):
    """
    API endpoint for students to upload their submissions.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        """
        Handle submission upload.
        """
        student = request.user.student

        submission, _ = Submission.objects.get_or_create(
            student = student,
            title=request.data.get('title', 'Untitled Submission'),
            defaults={'description': request.data.get('description', '')}
        )

        latest_version = submission.versions.order_by('-version').first()
        if latest_version:
            version_number = latest_version.version + 1
        else:
            version_number = 1

        submission_version = SubmissionVersion(
            submission=submission,
            version=version_number,
            docx_file=request.FILES['docx_file'],
            ppt_file=request.FILES['ppt_file'],
            similarity_report=request.FILES['similarity_report']
        )
        submission_version.save()

        try:
            similarity = extract_similarity_percentage(submission_version.similarity_report.path)
        except Exception as err:
            error = f" Could not extract similarity_report due to {err}"
            raise ValidationError({"similarity_report": error})

        submission_version.similarity_percentage = similarity
        if similarity <= 10:
            submission_version.status = 'Success'
            msg = "Submission uploaded successfully"
        else:
            submission_version.status = 'Failed'
            msg = "Similarity exceeds limit. Please re-upload all documents."
        submission_version.save()

        send_submission_email.delay(submission_version.id)

        return Response({
            "message": msg,
            "similarity_percentage": similarity,
            "status": submission_version.status
        })

class FacultyDashboardView(generics.ListAPIView):
    """
    API view for faculty to view submissions from their students.
    Provides a list of submissions for students assigned to the faculty.
    """
    serializer_class = SubmissionVersionSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Retrieves the queryset of submission versions for the students
        under the current faculty.
        """
        faculty = Faculty.objects.get(user=self.request.user)
        students = Student.objects.filter(faculty=faculty)
        if not students.exists():
            return SubmissionVersion.objects.none()
        return SubmissionVersion.objects.filter(submission__student__in=students)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        """
        Returns a response with a list of submission versions or
        an appropriate message if no students or submissions are found.
        """
        faculty = self.request.user.faculty
        students = Student.objects.filter(faculty=faculty)

        if not students.exists():
            return Response({
                "error": False,
                "status_code": 200,
                "message": "No students are currently assigned to you.",
                "data": []
            }, status=status.HTTP_200_OK)

        if not queryset.exists():
            return Response({
                "error": False,
                "status_code": 200,
                "message": "No submissions found for your students.",
                "data": []
            }, status=status.HTTP_200_OK)

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "error": False,
            "status_code": 200,
            "message": "Submissions fetched successfully.",
            "data": serializer.data
        }, status=status.HTTP_200_OK)


# class StudentSubmissionsView(generics.ListAPIView):
#     serializer_class = SubmissionSerializer
#
#     def get_queryset(self):
#         return Submission.objects.filter(student__user=self.request.user)

class StudentRegisterView(generics.CreateAPIView):
    """
    API view to register a student.
    """
    serializer_class = StudentRegisterSerializer
    queryset = Student.objects.all()
    authentication_classes = []

    def perform_create(self, serializer):
        """
        Creates a user and a student object.
        """
        username = serializer.validated_data.pop('username')
        password = serializer.validated_data.pop('password')
        user = User.objects.create_user(username=username, password=password)
        serializer.save(user=user)

class FacultyRegisterView(generics.CreateAPIView):
    """
    API view to register a faculty member.
    """
    serializer_class = FacultyRegisterSerializer
    queryset = Faculty.objects.all()
    authentication_classes = []

    def perform_create(self, serializer):
        """
        Creates a user and a faculty object.
        """
        username = serializer.validated_data.pop('username')
        password = serializer.validated_data.pop('password')
        user = User.objects.create_user(username=username, password=password, is_staff=True)
        serializer.save(user=user)

class FacultyListView(APIView):
    """
    API view to list all faculty members.
    """
    authentication_classes = []

    def get(self, request):
        """
        Returns a list of all faculty members.
        """
        faculties = Faculty.objects.all()
        serializer = FacultySerializer(faculties, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


