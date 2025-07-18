# Generated by Django 5.2.4 on 2025-07-17 21:37

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_alter_herovideo_thumbnail_alter_herovideo_video_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videoproject',
            name='thumbnail',
            field=cloudinary.models.CloudinaryField(blank=True, help_text='Upload thumbnail image (optional)', max_length=255, null=True, verbose_name='image'),
        ),
        migrations.AlterField(
            model_name='videoproject',
            name='video_file',
            field=cloudinary.models.CloudinaryField(help_text='Upload video file (mp4, mov, avi, mkv)', max_length=255, verbose_name='video'),
        ),
    ]
