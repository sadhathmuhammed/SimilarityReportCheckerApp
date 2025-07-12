from django.core.mail import send_mail
from django.conf import settings
from .models import SubmissionVersion
from similarity_report_checker.celery import app


@app.task
def send_submission_email(submission_version_id):
    """
    Send an email to the faculty when a student submits a new file.
    
    The email will contain the student's name, the timestamp of the submission,
    the similarity percentage, and links to the submitted files.
    """
    
    version = SubmissionVersion.objects.get(id=submission_version_id)
    faculty = version.submission.student.faculty

    message = f"""
    Hello {version.submission.student.faculty.name}
    
    Student {version.submission.student.name} has submitted an assignment with the following details:

    - Similarity: {version.similarity_percentage}%
    - Timestamp: {version.upload_timestamp}
    - Files:
        DOCX: {version.docx_file.url}
        PPTX: {version.ppt_file.url}
        Report: {version.similarity_report.url}
        
    Please log in to the faculty dashboard to review the full submission.

    Regards,
    Assignment Portal


    """

    send_mail(
        subject=f"Assignment Submission from {version.submission.student.name} – Similarity: {version.similarity_percentage}%",
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[faculty.email]
    )
