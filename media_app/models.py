from django.db import models

class MediaFile(models.Model):
    MEDIA_TYPES = [
        ('image', 'Image'),
        ('video', 'Video'),
        ('carousel', 'Carousel'),
    ]

    file = models.FileField(upload_to='uploads/%Y/%m/')
    media_type = models.CharField(max_length=20, choices=MEDIA_TYPES)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name
