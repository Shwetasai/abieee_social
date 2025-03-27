from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

PLATFORM_CHOICES = [
    ('linkedin', 'LinkedIn'),
    ('facebook', 'Facebook'),
    ('instagram', 'Instagram'),
    ('tiktok', 'TikTok'),
]

SOURCE_TYPE_CHOICES = [
    ('system', 'System'),
    ('self', 'Self'),
]

class SchedulingPreferences(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    days_hours = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class PostDistribution(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    total_posts = models.IntegerField()
    test_posts = models.IntegerField(blank=True, null=True)
    image_posts = models.IntegerField(blank=True, null=True)
    video_posts = models.IntegerField(blank=True, null=True)
    reel_posts = models.IntegerField(blank=True, null=True)

    image_source = models.CharField(max_length=10, choices=SOURCE_TYPE_CHOICES, default='self')
    video_source = models.CharField(max_length=10, choices=SOURCE_TYPE_CHOICES, default='self')
    reels_source = models.CharField(max_length=10, choices=SOURCE_TYPE_CHOICES, default='self')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

