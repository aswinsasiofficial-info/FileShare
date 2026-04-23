# Project Documentation: Fileshare

A comprehensive guide to the **Fileshare** web application, covering its architecture, features, security, and deployment for theoretical study.

---

## 1. Project Overview
**Fileshare** is a secure, modern file-sharing platform built with Python (Django). It allows users to register accounts, upload files of various formats, and generate unique, shareable links for public access.

### Key Objectives:
- Provide a simple, responsive interface for file management.
- Ensure secure storage and controlled access to files.
- Enable easy sharing without requiring the recipient to log in.

---

## 2. Technical Stack
- **Backend Framework**: Django 6.0.4 (Python)
- **Database**: SQLite (Local) / PostgreSQL (Production on Render)
- **Frontend**: HTML5, CSS3, JavaScript (ES6+), Bootstrap 5
- **Styling/Icons**: Bootstrap Icons, Custom "Inter Tight" Typography
- **Deployment**: Render (Gunicorn, WhiteNoise, Persistent Disk)

---

## 3. Project Architecture (MVT Pattern)
Django follows the **Model-View-Template (MVT)** architectural pattern:

1.  **Model**: Defines the data structure (Database).
    - Located in `files/models.py` and `accounts/models.py`.
2.  **View**: Contains the business logic and handles requests.
    - Located in `files/views.py` and `accounts/views.py`.
3.  **Template**: The presentation layer (HTML).
    - Located in the root `templates/` directory.

---

## 4. Database Schema
### SharedFile Model (`files/models.py`)
| Field | Type | Description |
| :--- | :--- | :--- |
| `id` | UUID | Primary Key, unique identifier for sharing URLs. |
| `owner` | ForeignKey | Links the file to a specific `User`. |
| `file` | FileField | Path to the physical file in storage. |
| `original_name`| CharField | The name of the file as uploaded by the user. |
| `file_type` | CharField | MIME type (e.g., image/png, application/pdf). |
| `file_size` | BigIntegerField| Size of the file in bytes. |
| `upload_timestamp`| DateTime | Automatically set when the file is uploaded. |
| `expires_at` | DateTime | Optional expiration date for the link. |
| `download_count`| Integer | Tracks how many times the file was downloaded. |

---

## 5. Core Features & Logic Flow

### A. Authentication System
- **Registration**: Uses a custom `UserRegistrationForm` to collect email and password. Behind the scenes, the email is synced to the Django `username` field to maintain compatibility.
- **Login/Logout**: Leverages Django's built-in `auth` views for session-based security, using Email as the primary identifier.
- **Access Control**: The `@login_required` decorator protects the home page and management actions.

### B. File Upload System
1. **Drag & Drop**: JavaScript (XHR/Fetch) handles the file selection and upload progress.
2. **Sanitization**: Filenames are renamed to unique UUIDs on the server to prevent directory traversal attacks and name collisions.
3. **Validation**: Enforces a 100MB file size limit.

### C. Sharing & Public Access
- **UUID URLs**: Sharing links use the file's UUID (e.g., `/s/d27682b8.../`) instead of predictable integer IDs.
- **Public View**: A dedicated view (`public_file_view`) allows anyone with the link to see metadata.
- **Secure Download**: Files are served through a Django view (`download_file`) using `FileResponse`, allowing for future access logic (like expiration checks).

---

## 6. Security Implementation
- **CSRF Protection**: Prevents Cross-Site Request Forgery on all forms.
- **Path Protection**: Files are stored in a `media/` directory that is not directly browseable; access is controlled via views.
- **Password Hashing**: User passwords (and previously share passwords) are hashed using industry-standard algorithms (PBKDF2).
- **Human-Readable Timestamps**: Uses `django.contrib.humanize` to make timestamps user-friendly.

---

## 7. Deployment Configuration
- **Render.yaml**: Defines the infrastructure, including the web service and a persistent disk to ensure uploaded files aren't lost when the server restarts.
- **Build.sh**: Automates the installation of dependencies, database migrations, and static file collection.
- **WhiteNoise**: Configured to serve static files (CSS, JS, Fonts) efficiently in a production environment.

---

## 8. Theoretical Study Concepts
- **RESTful Principles**: The use of clean URLs and standard HTTP methods (GET for viewing, POST for uploading/deleting).
- **Session Management**: How Django uses cookies and database sessions to keep users logged in.
- **Blob Storage**: The concept of handling binary data separately from the relational database metadata.
- **Middleware**: Using WhiteNoise middleware to intercept requests for static files.
