from django.urls import path
from . import views

app_name = 'files'

urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.upload_file, name='upload'),
    path('delete/<uuid:file_id>/', views.delete_file, name='delete'),
    path('s/<uuid:file_id>/', views.public_file_view, name='public_view'),
    path('d/<uuid:file_id>/', views.download_file, name='download'),
]
