# core/admin.py
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.contrib import messages
from .models import AboutSection, ContactMessage, ExperienceHighlight, Expertise, HeroVideo, Skill, SkillCategory, Tool, VideoProject

@admin.register(HeroVideo)
class HeroVideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'created_at', 'updated_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Video Information', {
            'fields': ('title', 'description', 'is_active')
        }),
        ('Files', {
            'fields': ('video_file', 'thumbnail')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        try:
            super().save_model(request, obj, form, change)
            messages.success(request, "Hero video saved successfully!")
        except ValidationError as e:
            messages.error(request, str(e))
    
    def has_add_permission(self, request):
        # Only allow adding if no hero video exists
        return not HeroVideo.objects.exists()
    
    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(super().get_readonly_fields(request, obj))
        
        # If this is the only video, make is_active readonly (must stay True)
        if obj and HeroVideo.objects.count() == 1:
            readonly_fields.append('is_active')
        
        return readonly_fields
    

@admin.register(VideoProject)
class VideoProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'get_duration_display', 'is_featured', 'created_at', 'order']
    list_filter = ['is_featured', 'created_at']
    search_fields = ['title', 'description', 'tags']
    list_editable = ['is_featured', 'order']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'tags')
        }),
        ('Media Files', {
            'fields': ('video_file', 'thumbnail')
        }),
        ('Settings', {
            'fields': ('duration', 'is_featured', 'order')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_duration_display(self, obj):
        return obj.get_duration_display()
    get_duration_display.short_description = 'Duration'


class SkillInline(admin.TabularInline):
    model = Skill
    extra = 1

@admin.register(SkillCategory)
class SkillCategoryAdmin(admin.ModelAdmin):
    inlines = [SkillInline]

admin.site.register(Tool)
admin.site.register(ExperienceHighlight)

class ExpertiseInline(admin.TabularInline):
    model = Expertise
    extra = 1

@admin.register(AboutSection)
class AboutSectionAdmin(admin.ModelAdmin):
    inlines = [ExpertiseInline]


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    search_fields = ('name', 'email', 'subject')
    ordering = ('-created_at',)