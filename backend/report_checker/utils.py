import fitz
import docx
import re

from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    """
    Custom exception handler to include status code in the response.
    """
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
    """
    Extracts the similarity percentage from a given document file.

    This function reads the content of a file, either a PDF or DOCX, and searches
    for a similarity percentage value stated in the format of "xx.xx% SIMILARITY".
    It returns the extracted percentage as a float. If no such pattern is found,
    it returns 0.0.

    Args:
        file_path (str): The path to the document file (.pdf or .docx).

    Returns:
        float: The extracted similarity percentage, or 0.0 if not found.
    """

    text = ""
    if file_path.endswith('.pdf'):
        doc = fitz.open(file_path)
        text = "".join(page.get_text() for page in doc)
    elif file_path.endswith('.docx'):
        document = docx.Document(file_path)
        text = "\n".join([p.text for p in document.paragraphs])
    match = re.search(r'(\d{1,3}(?:\.\d+)?)%\s+SIMILARITY', text, re.IGNORECASE)
    return float(match.group(1)) if match else 0.0
