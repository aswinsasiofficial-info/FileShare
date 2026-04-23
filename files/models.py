from django.db import models
from django.contrib.auth.models import User
import uuid
import os

class SharedFile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='uploads/%Y/%m/%d/')
    original_name = models.CharField(max_length=255)
    file_type = models.CharField(max_length=100)
    file_size = models.BigIntegerField()
    upload_timestamp = models.DateTimeField(auto_now_add=True)
    
    # Optional: Expiry
    expires_at = models.DateTimeField(blank=True, null=True)
    # Download count
    download_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.original_name

    def delete(self, *args, **kwargs):
        # Delete the actual file from storage when model is deleted
        if self.file:
            if os.path.isfile(self.file.path):
                os.remove(self.file.path)
        super().delete(*args, **kwargs)

    @property
    def extension(self):
        name, extension = os.path.splitext(self.file.name)
        return extension.lower()
