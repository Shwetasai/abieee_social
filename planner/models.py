from django.db import models
from django.conf import settings
import uuid
PLATFORM_CHOICES = [
    ('linkedin', 'LinkedIn'),
    ('facebook', 'Facebook'),
    ('instagram', 'Instagram'),
    ('tiktok', 'TikTok'),
]

POST_TYPE_CHOICES = [
    ('image_post', 'Image Post'),
    ('video_post', 'Video Post'),
    ('text_post', 'Text Post'),
    ('reel', 'Reel'),
]

UPLOAD_TYPE_CHOICES = [
    ('system', 'System'),
    ('self', 'Self'),
]

class PendingPost(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    publication_date = models.DateField()
    publication_time = models.TimeField()
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    post_type = models.CharField(max_length=20, choices=POST_TYPE_CHOICES)
    upload_type = models.CharField(max_length=10, choices=UPLOAD_TYPE_CHOICES, default='self')
    created_at = models.DateTimeField(auto_now_add=True)
    post_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    def __str__(self):
        return f"{self.user} - {self.platform} ({self.post_type})"

class Post(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('canceled', 'Canceled')
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.TextField()
    media = models.ImageField(upload_to="posts/", blank=True, null=True)
    post_type = models.CharField(max_length=50, choices=POST_TYPE_CHOICES)
    platform = models.CharField(max_length=50, choices=PLATFORM_CHOICES)
    scheduling_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    
    def __str__(self):
        return f"{self.content[:30]} ({self.status})"