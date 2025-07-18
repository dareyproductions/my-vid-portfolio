# Generated by Django 5.2.4 on 2025-07-17 23:32

import cloudinary.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_alter_videoproject_thumbnail_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videoproject',
            name='tags',
            field=models.CharField(help_text='Comma-separated tags', max_length=500),
        ),
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
