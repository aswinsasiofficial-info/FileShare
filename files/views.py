from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404, FileResponse
from django.contrib import messages
from .models import SharedFile
from django.utils import timezone
import os
import uuid

@login_required
def home(request):
    files = request.user.files.all().order_by('-upload_timestamp')
    return render(request, 'files/home.html', {'files': files})

@login_required
def upload_file(request):
    if request.method == 'POST':
        uploaded_file = request.FILES.get('file')
        expiry_days = request.POST.get('expiry_days')

        if not uploaded_file:
            messages.error(request, "No file uploaded.")
            return redirect('files:home')

        # Limit file size: 100MB
        if uploaded_file.size > 100 * 1024 * 1024:
            messages.error(request, "File too large (max 100MB).")
            return redirect('files:home')

        # Calculate expiry
        expires_at = None
        if expiry_days and expiry_days.isdigit():
            expires_at = timezone.now() + timezone.timedelta(days=int(expiry_days))

        # Sanitize filename (basic)
        ext = os.path.splitext(uploaded_file.name)[1]
        unique_name = f"{uuid.uuid4()}{ext}"
        uploaded_file.name = unique_name

        shared_file = SharedFile.objects.create(
            owner=request.user,
            file=uploaded_file,
            original_name=uploaded_file.name,
            file_type=uploaded_file.content_type,
            file_size=uploaded_file.size,
            expires_at=expires_at
        )
        
        # Restore original name for display
        shared_file.original_name = request.FILES.get('file').name
        shared_file.save()

        messages.success(request, f'File "{shared_file.original_name}" uploaded successfully!')
        return redirect('files:home')
    
    return redirect('files:home')

@login_required
def delete_file(request, file_id):
    shared_file = get_object_or_404(SharedFile, id=file_id, owner=request.user)
    shared_file.delete()
    messages.success(request, "File deleted successfully.")
    return redirect('files:home')

def public_file_view(request, file_id):
    shared_file = get_object_or_404(SharedFile, id=file_id)
    
    # Check expiry
    if shared_file.expires_at and shared_file.expires_at < timezone.now():
        messages.error(request, "This link has expired.")
        raise Http404("File link has expired.")

    return render(request, 'files/public_view.html', {'file': shared_file})

def download_file(request, file_id):
    shared_file = get_object_or_404(SharedFile, id=file_id)
    
    # Check expiry
    if shared_file.expires_at and shared_file.expires_at < timezone.now():
        raise Http404("File link has expired.")

    # Increment download count
    shared_file.download_count += 1
    shared_file.save()

    # Serve the file securely
    response = FileResponse(shared_file.file.open(), as_attachment=True, filename=shared_file.original_name)
    return response
