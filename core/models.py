# core/models.py
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from cloudinary.models import CloudinaryField
from cloudinary.utils import cloudinary_url
from cloudinary.models import CloudinaryField

class HeroVideo(models.Model):
    title = models.CharField(max_length=200, default="Demo Reel")
    description = models.TextField(blank=True, null=True)

    video_file = CloudinaryField(
        resource_type='video',
        validators=[FileExtensionValidator(allowed_extensions=['mp4', 'webm', 'ogg'])],
        help_text="Upload video file (MP4, WebM, or OGG format)"
    )

    thumbnail = CloudinaryField(
        resource_type='image',
        blank=True,
        null=True,
        help_text="Optional thumbnail image"
    )

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Hero Video"
        verbose_name_plural = "Hero Videos"

    def __str__(self):
        return self.title

    def clean(self):
        if self.is_active:
            existing_active = HeroVideo.objects.filter(is_active=True)
            if self.pk:
                existing_active = existing_active.exclude(pk=self.pk)
            if existing_active.exists():
                raise ValidationError("Only one hero video can be active at a time.")

    def save(self, *args, **kwargs):
        if not self.pk and HeroVideo.objects.count() >= 1:
            raise ValidationError("Only one hero video is allowed. Please delete the existing video first.")
        self.clean()
        super().save(*args, **kwargs)

    @classmethod
    def get_active_video(cls):
        try:
            return cls.objects.get(is_active=True)
        except cls.DoesNotExist:
            return None

        



# core/models.py
from django.db import models
from django.core.validators import FileExtensionValidator
import os

class VideoProject(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    # Video file
    video_file = CloudinaryField(
        resource_type='video',
        validators=[FileExtensionValidator(allowed_extensions=['mp4', 'mov', 'avi', 'mkv'])],
        help_text="Upload video file (mp4, mov, avi, mkv)"
    )
    
    # Thumbnail image (optional - can be auto-generated)
    thumbnail = CloudinaryField(
        resource_type='image',
        blank=True,
        null=True,
        help_text="Upload thumbnail image (optional)"
    )
    
    # Duration in seconds
    duration = models.PositiveIntegerField(
        help_text="Duration in seconds"
    )
    
    # Tags for the project
    tags = models.CharField(
        max_length=500,
        help_text="Comma-separated tags (e.g., 'Premiere Pro, After Effects, Color Grading')"
    )
    
    # Additional fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0, help_text="Order for display")
    
    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = "Video Project"
        verbose_name_plural = "Video Projects"
    
    def __str__(self):
        return self.title
    
    def get_tags_list(self):
        """Return tags as a list"""
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]
    
    def get_duration_display(self):
        """Convert duration in seconds to MM:SS format"""
        minutes = self.duration // 60
        seconds = self.duration % 60
        return f"{minutes}:{seconds:02d}"
    

    def get_video_url(self):
        if self.video_file:
            url, options = cloudinary_url(
                self.video_file.name,
                resource_type="video"
            )
            return url
        return None

    
    def get_thumbnail_url(self):
        """Get the thumbnail URL"""
        if self.thumbnail:
            return self.thumbnail.url
        return None
    

class Tool(models.Model):
    name = models.CharField(max_length=100)
    badge = models.CharField(max_length=50)  # e.g., "Video Editing"
    description = models.TextField()
    proficiency = models.PositiveIntegerField(default=0)
    icon_svg = models.TextField(help_text="Paste inline SVG code here")

    def __str__(self):
        return self.name


class SkillCategory(models.Model):
    title = models.CharField(max_length=100)
    icon_svg = models.TextField(help_text="Paste inline SVG icon")
    
    def __str__(self):
        return self.title


class Skill(models.Model):
    category = models.ForeignKey(SkillCategory, related_name='skills', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.category.title} - {self.name}"


class ExperienceHighlight(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon_svg = models.TextField(help_text="Paste inline SVG icon")

    def __str__(self):
        return self.title



class AboutSection(models.Model):
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)
    cv_file = models.FileField(upload_to='cvs/', null=True, blank=True)
    about_text_1 = models.TextField()
    about_text_2 = models.TextField(blank=True)
    about_text_3 = models.TextField(blank=True)

    # Stats
    years_experience = models.CharField(max_length=10, default="4+")
    projects_completed = models.CharField(max_length=10, default="65+")
    happy_clients = models.CharField(max_length=10, default="25+")
    coffee_consumed = models.CharField(max_length=10, default="∞")

    def save(self, *args, **kwargs):
        if not self.pk and AboutSection.objects.exists():
            raise ValidationError('Only one AboutSection instance is allowed.')
        return super().save(*args, **kwargs)


    def __str__(self):
        return "About Section"


class Expertise(models.Model):
    about = models.ForeignKey(AboutSection, on_delete=models.CASCADE, related_name='expertise')
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name



class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=150)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"