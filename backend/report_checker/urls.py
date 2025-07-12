from django.urls import path
from .views import (
    StudentRegisterView,
    FacultyRegisterView,
    LoginView,
    StudentUploadView,
    FacultyDashboardView, FacultyListView,
)

urlpatterns = [
    path('auth/register/student/', StudentRegisterView.as_view(), name='register-student'),
    path('auth/register/faculty/', FacultyRegisterView.as_view(), name='register-faculty'),
    path('auth/login/', LoginView.as_view(), name='login'),

    path('student/upload/', StudentUploadView.as_view(), name='student-upload'),
    # path('student/submissions/', StudentSubmissionsView.as_view(), name='student-submissions'),

    path('faculty/dashboard/', FacultyDashboardView.as_view(), name='faculty-dashboard'),
    path('faculty/list/', FacultyListView.as_view(), name='faculty-list')

]