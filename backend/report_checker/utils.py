import fitz
import docx
import re

from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        if response.status_code == 401:
            response.data = {
                "error": True,
                "status_code": 401,
                "message": "Invalid or expired token. Please login again."
            }
        elif response.status_code == 403:
            response.data = {
                "error": True,
                "status_code": 403,
                "message": "You do not have permission to access this resource."
            }
        else:
            response.data['status_code'] = response.status_code
            response.data['error'] = True

    return response

def extract_similarity_percentage(file_path):
    text = ""
    if file_path.endswith('.pdf'):
        doc = fitz.open(file_path)
        text = "".join(page.get_text() for page in doc)
    elif file_path.endswith('.docx'):
        document = docx.Document(file_path)
        text = "\n".join([p.text for p in document.paragraphs])
    match = re.search(r'(\d{1,3}(?:\.\d+)?)%\s+SIMILARITY', text, re.IGNORECASE)
    return float(match.group(1)) if match else 0.0
