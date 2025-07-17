# core/views.py
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.core.files.storage import default_storage
from django.conf import settings
import json
import os
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views import View
from django.core.mail import EmailMessage
from django.utils.decorators import method_decorator
from .models import AboutSection, ContactMessage, ExperienceHighlight, HeroVideo, SkillCategory, Tool, VideoProject

def home(request):

    """Render the home page with hero video data"""
    hero_video = HeroVideo.get_active_video()

    """Home page view with video projects"""
    projects = VideoProject.objects.all()

    tools = Tool.objects.all()
    skill_categories = SkillCategory.objects.prefetch_related('skills')
    highlights = ExperienceHighlight.objects.all()

    
    about = AboutSection.objects.first()


    context = {
        'hero_video': hero_video,
        'has_video': hero_video is not None,
        'projects': projects,
        "tools": tools,
        "skill_categories": skill_categories,
        "highlights": highlights,
        'about': about,
    }

    

    return render(request, 'index.html', context)

def get_hero_video_data(request):
    """API endpoint to get hero video data as JSON"""
    hero_video = HeroVideo.get_active_video()
    
    if hero_video:
        data = {
            'has_video': True,
            'title': hero_video.title,
            'description': hero_video.description,
            'video_url': hero_video.video_file.url,
            'thumbnail_url': hero_video.thumbnail.url if hero_video.thumbnail else None,
            'created_at': hero_video.created_at.isoformat(),
        }
    else:
        data = {
            'has_video': False,
            'title': 'Demo Reel Coming Soon',
            'description': 'Click to watch showreel',
            'video_url': None,
            'thumbnail_url': None,
        }
    
    return JsonResponse(data)

@login_required
@require_http_methods(["POST"])
@csrf_exempt
def upload_hero_video(request):
    """Upload a new hero video (admin only)"""
    if not request.user.is_staff:
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    # Check if video already exists
    if HeroVideo.objects.exists():
        return JsonResponse({'error': 'Hero video already exists. Delete it first.'}, status=400)
    
    if 'video_file' not in request.FILES:
        return JsonResponse({'error': 'No video file provided'}, status=400)
    
    video_file = request.FILES['video_file']
    title = request.POST.get('title', 'Demo Reel')
    description = request.POST.get('description', '')
    thumbnail = request.FILES.get('thumbnail', None)
    
    try:
        hero_video = HeroVideo.objects.create(
            title=title,
            description=description,
            video_file=video_file,
            thumbnail=thumbnail,
            is_active=True
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Hero video uploaded successfully',
            'video_id': hero_video.id,
            'video_url': hero_video.video_file.url
        })
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@login_required
@require_http_methods(["DELETE"])
def delete_hero_video(request):
    """Delete the hero video (admin only)"""
    if not request.user.is_staff:
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    hero_video = HeroVideo.get_active_video()
    if not hero_video:
        return JsonResponse({'error': 'No hero video found'}, status=404)
    
    # Delete the file from storage
    if hero_video.video_file:
        default_storage.delete(hero_video.video_file.name)
    if hero_video.thumbnail:
        default_storage.delete(hero_video.thumbnail.name)
    
    hero_video.delete()
    
    return JsonResponse({
        'success': True,
        'message': 'Hero video deleted successfully'
    })

@login_required
def admin_hero_video(request):
    """Admin page for managing hero video"""
    if not request.user.is_staff:
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    hero_video = HeroVideo.get_active_video()
    context = {
        'hero_video': hero_video,
        'has_video': hero_video is not None,
    }
    return render(request, 'admin_hero_video.html', context)



def project_detail(request, project_id):
    """Individual project detail view"""
    project = get_object_or_404(VideoProject, id=project_id)
    context = {
        'project': project,
    }
    return render(request, 'project_detail.html', context)

def get_video_url(request, project_id):
    """API endpoint to get video URL for streaming"""
    project = get_object_or_404(VideoProject, id=project_id)
    return JsonResponse({
        'video_url': project.get_video_url(),
        'title': project.title,
        'description': project.description,
    })



class ContactFormView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            name = data.get('name')
            email = data.get('email')
            subject = data.get('subject')
            message = data.get('message')

            # Save to database
            ContactMessage.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message
            )

            # Send email
            full_message = f"From: {name}\nEmail: {email}\n\nMessage:\n{message}"
            email_obj = EmailMessage(
                subject=subject,
                body=full_message,
                from_email='your_email@gmail.com',  # Must still be the Gmail account you're authenticated with
                to=['dareyproductions@gmail.com'],
                reply_to=[email],  # 👈 Now works
            )
            email_obj.send(fail_silently=False)

            return JsonResponse({'success': True, 'message': 'Message sent and saved.'})

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)


from django.contrib.auth import get_user_model
from django.http import HttpResponse

def create_superuser_once(request):
    User = get_user_model()
    if User.objects.filter(email="admin@example.com").exists():
        return HttpResponse("Superuser already exists.")

    User.objects.create_superuser(
        email="dareyproductions@gmail.com",
        username="dareyproductions",
        password="Dareyproductions7#",
        first_name="Darey",
        last_name="Productions"
    )
    return HttpResponse("Superuser created successfully.")
