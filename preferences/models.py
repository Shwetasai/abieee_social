from django.db import models
from django.conf import settings

class SchedulingPreferences(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    platforms = models.JSONField()
    days_hours = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

class PostDistribution(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    total_posts = models.IntegerField()
    test_posts = models.IntegerField(blank=True, null=True)
    image_posts = models.IntegerField(blank=True, null=True)
    video_posts = models.IntegerField(blank=True, null=True)
    reel_posts = models.IntegerField(blank=True, null=True)
    image_source = models.CharField(max_length=10, choices=[('system', 'System'), ('self', 'Self')], default='self')
    video_source = models.CharField(max_length=10, choices=[('system', 'System'), ('self', 'Self')], default='self')
    reels_source = models.CharField(max_length=10, choices=[('system', 'System'), ('self', 'Self')], default='self')
    created_at = models.DateTimeField(auto_now_add=True)