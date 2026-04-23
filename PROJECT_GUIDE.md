# Project Documentation: Fileshare

A comprehensive guide to the **Fileshare** web application, covering its architecture, features, security, and deployment for theoretical study.

---

## 1. Project Overview
**Fileshare** is a secure, modern file-sharing platform built with Python (Django). It allows users to register accounts using only their email, upload files of various formats, and generate unique, shareable links for public access.

### Key Objectives:
- Provide a minimalist, mobile-responsive interface for file management.
- Ensure secure storage and controlled access to files via unique UUIDs.
- Enable instant sharing and file previews without complex requirements.

---

## 2. Technical Stack
- **Backend Framework**: Django 6.0.4 (Python)
- **Authentication**: Custom Email-based Backend (`accounts.backends.EmailBackend`)
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

### A. Authentication System (Email-Only)
- **Registration**: Users register with just an **Email** and **Password**. The email is automatically synced to the Django `username` field to maintain system compatibility.
- **Login**: A custom authentication backend allows logging in with either email or username.
- **Access Control**: Secure session management ensures only owners can delete or manage their files.

### B. File Upload System
1. **Drag & Drop**: A JavaScript-powered upload zone provides a real-time progress bar.
2. **Sanitization**: Files are renamed using UUIDs to prevent path guessing and security vulnerabilities.
3. **Validation**: Enforces a 100MB file size limit.

### C. Sharing & Viewing
- **UUID URLs**: Sharing links use secure, non-predictable UUIDs.
- **View Modal**: Users can preview files (with automatic image support) directly on the home page via a popup modal.
- **Public View**: A compact, mobile-friendly page for public downloads.

### D. Admin Panel
- **Custom Dashboard**: Superusers can access a dedicated `/accounts/users/` panel to monitor registered users and their file upload counts.
- **Security**: Restricted to superusers using strict Django decorators.

---

## 6. Security Implementation
- **CSRF Protection**: Enabled for all data submissions and AJAX uploads.
- **Multiple Backends**: Uses a prioritized `EmailBackend` with the standard `ModelBackend` as a fallback.
- **Path Protection**: Files are served through Django views, allowing the application to enforce access rules (like expiration).
- **Human-Readable Timestamps**: Uses `naturaltime` (e.g., "5 minutes ago") for a better user experience.

---

## 7. Deployment Configuration
- **Render.yaml**: Configured for Render's cloud platform, including persistent disk storage for uploaded files.
- **Build Script**: Automates dependency installation, migrations, and static file collection (`build.sh`).
- **Production Efficiency**: Uses **WhiteNoise** for high-performance static file serving and **Gunicorn** as the production server.

---

## 8. Theoretical Study Concepts
- **Custom Backends**: Extending Django's authentication system to change how users are identified.
- **MVT Data Flow**: How data travels from the SQLite database through UUID-filtered views to Bootstrap templates.
- **Asynchronous UI**: Using JavaScript XHR to handle file uploads without refreshing the page.
- **Responsive Design**: Implementing mobile-first grid systems to ensure accessibility across all devices.
