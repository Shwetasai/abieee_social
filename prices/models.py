from django.db import models
from django.conf import settings
#from datetime import date, timedelta
class Package(models.Model):
    class PackageType(models.TextChoices):
        PREMIUM = "Premium", "Premium"
        ADVANCED = "Advanced", "Advanced"
        STANDARD = "Standard", "Standard"
        BEGINNERS = "Beginners", "Beginners"

    package_type = models.CharField(
        max_length=10, choices=PackageType.choices, unique=True
    )
    price = models.IntegerField()
    platforms = models.CharField(max_length=255)
    posts_per_month = models.IntegerField()
    credits = models.IntegerField()
    content_text = models.BooleanField(default=True)
    content_photos = models.BooleanField(default=True)
    content_video = models.BooleanField(default=True)
    editing = models.CharField(max_length=100, choices=[("Before approval", "Before approval"), ("Before and after approval", "Before and After approval")])
    history = models.CharField(max_length=50)

    def __str__(self):
        return self.package_type
    
