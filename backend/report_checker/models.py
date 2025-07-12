from django.db import models
from django.contrib.auth.models import User

class Faculty(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='faculty')
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    department = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student')
    student_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='student')

    def __str__(self):
        return f"{self.name} (ID: {self.student_id})"

class Submission(models.Model):
    submission_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='submissions')
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"Submission {self.submission_id} - {self.title} - Student {self.student.student_id}"

    @property
    def latest_version(self):
        return self.versions.order_by('-version').first()

def submission_upload_path(instance, filename):
    return f"submissions/student_{instance.submission.student.student_id}/submission_{instance.submission.submission_id}/v{instance.version}/{filename}"

class SubmissionVersion(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name='versions')
    version = models.PositiveIntegerField()
    docx_file = models.FileField(upload_to=submission_upload_path)
    ppt_file = models.FileField(upload_to=submission_upload_path)
    similarity_report = models.FileField(upload_to=submission_upload_path)
    upload_timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[
        ('Pending', 'Pending'),
        ('Success', 'Success'),
        ('Not Success', 'Not Success')
    ], default='Pending')
    remarks = models.TextField(blank=True)
    similarity_percentage = models.FloatField(default=0.0)

    class Meta:
        unique_together = ('submission', 'version')
        ordering = ['version']

    def __str__(self):
        return f"{self.submission.submission_id} - v{self.version}"


