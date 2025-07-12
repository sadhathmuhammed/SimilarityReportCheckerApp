from django.core.mail import send_mail
from django.conf import settings
from .models import SubmissionVersion
from similarity_report_checker.celery import app


@app.task
def send_submission_email(submission_version_id):
    version = SubmissionVersion.objects.get(id=submission_version_id)
    faculty = version.submission.student.faculty

    message = f"""
    New submission by {version.submission.student.name}
    Timestamp: {version.upload_timestamp}
    Similarity: {version.similarity_percentage}%
    Files:
    DOCX: {version.docx_file.url}
    PPTX: {version.ppt_file.url}
    Report: {version.similarity_report.url}
    """

    send_mail(
        subject=f"New Submission from {version.submission.student.name}",
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[faculty.email]
    )
