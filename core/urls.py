# core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Public endpoints
    path('', views.home, name='home'),
    path('api/hero-video/', views.get_hero_video_data, name='get_hero_video_data'),
    
    # Debug endpoint (remove this after debugging)
    # path('debug/media/', views.debug_media, name='debug_media'),
    
    # Admin endpoints
    path('admin/hero-video/', views.admin_hero_video, name='admin_hero_video'),
    path('api/upload-hero-video/', views.upload_hero_video, name='upload_hero_video'),
    path('api/delete-hero-video/', views.delete_hero_video, name='delete_hero_video'),

    # Viseo portfolio endpoints
    path('project/<int:project_id>/', views.project_detail, name='project_detail'),
    path('api/video/<int:project_id>/', views.get_video_url, name='get_video_url'),


    path('contact/send/', views.ContactFormView.as_view(), name='contact_send'),
    # path('create-superuser/', views.create_superuser_once, name='create_superuser'),
]