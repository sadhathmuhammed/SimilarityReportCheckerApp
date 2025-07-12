# 📁 Similarity Report Checker Portal

A **full-stack application** for managing project submissions with similarity checking, built using:

- 🐍 Django (REST API)
- ⚛️ React JS(Frontend)
- ✉️ Celery + Redis (for sending emails)
- 📦 SQLite (Database)

Students can upload project files, and similarity reports are checked automatically. Faculty can view student submissions, and email notifications are sent on successful uploads.

---

## 🚀 Features

✅ Student and Faculty Registration/Login (JWT Authentication)  
✅ Students upload DOCX, PPTX, and Similarity Report (PDF/DOCX)  
✅ Automatic similarity check (if % > 10%, re-upload required)  
✅ Versioning of submissions  
✅ Faculty Dashboard with all student submissions  
✅ Email notifications using Celery + Redis  
✅ Rate Limiting and Pagination on APIs  

---
## ⚙️ Redis + Celery Setup Guide

This project uses **Celery** for background task processing and **Redis** as the message broker. It handles tasks like **sending emails after a submission**.

---

## 📦 Tech Stack

| Layer           | Tech                        |
|-----------------|-----------------------------|
| Backend         | Django REST Framework (DRF) |
| Frontend        | React.js                    |
| Database        | SQLite (local)              |
| Background Jobs | Celery + Redis              |
| Emails          | Gmail SMTP                  |
---


## ⚙️ Setup Guide

### 🐳 Prerequisites
- Python
- Node.js & npm (if running frontend separately)
- React js
- Sqlite db

### 🚀 Local Development

1. Clone the repository:
   ```bash
   git clone https://github.com/sadhathmuhammed/SimilarityReportCheckerApp.git
   cd SimilarityReportCheckerApp
   ```
2. Backend 
    ```bash
    cd backend
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    python manage.py migrate
    python manage.py runserver 
    ```
    ```bash
    celery -A similarity_report_checker worker -l info
    ```
3. Frontend
    ```bash
       cd frontend
       npm install
       npm start
      ```


