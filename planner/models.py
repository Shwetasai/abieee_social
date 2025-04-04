from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
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
STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('canceled', 'Canceled')
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
    content_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    media_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    media = models.ImageField(upload_to="pending_posts/", blank=True, null=True)

    

    def clean(self):
        valid_platforms = dict(PLATFORM_CHOICES).keys()
        valid_post_types = dict(POST_TYPE_CHOICES).keys()
        
        if self.platform not in valid_platforms:
            raise ValidationError(f"Invalid platform: {self.platform}. Choose from {', '.join(valid_platforms)}.")
        
        if self.post_type not in valid_post_types:
            raise ValidationError(f"Invalid post type: {self.post_type}. Choose from {', '.join(valid_post_types)}.")

    def __str__(self):
        return f"{self.user} - {self.platform} ({self.post_type})"
    
class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.TextField()
    media = models.ImageField(upload_to="posts/", blank=True, null=True)
    post_type = models.CharField(max_length=50, choices=POST_TYPE_CHOICES)
    platform = models.CharField(max_length=50, choices=PLATFORM_CHOICES)
    scheduling_date = models.DateTimeField()
    
    def clean(self):
        valid_platforms = dict(PLATFORM_CHOICES).keys()
        if self.platform not in valid_platforms:
            raise ValidationError(f"Invalid platform: {self.platform}. Choose from {', '.join(valid_platforms)}.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} - {self.platform})"

