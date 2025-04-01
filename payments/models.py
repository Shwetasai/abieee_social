from django.db import models
import uuid
from prices.models import Package
from django.conf import settings
from datetime import date, timedelta
from django.utils import timezone
class CardInformation(models.Model):
    amount = models.IntegerField()
    currency = models.CharField(max_length=3, default='usd')

    def __str__(self):
        return f"Card: **** **** **** {self.card_number[-4:]}"

class Payment(models.Model):
    payment_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    card_info = models.ForeignKey(CardInformation, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name="payments")
    payment_intent_id = models.CharField(max_length=255, blank=True, null=True)
    amount = models.IntegerField()
    currency = models.CharField(max_length=3)
    payment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='pending') 

    def __str__(self):
        return f"Payment ID: {self.payment_id}"
    
class UserPackage(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    package_type = models.CharField(max_length=100)
    price = models.IntegerField()
    platforms = models.CharField(max_length=50)
    posts_per_month = models.IntegerField()
    credits = models.IntegerField()
    content_text = models.BooleanField()
    content_photos = models.BooleanField()
    content_video = models.BooleanField()
    editing = models.CharField(max_length=255)
    history = models.CharField(max_length=50)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()

    def save(self, *args, **kwargs):
        existing_package = UserPackage.objects.filter(user=self.user).order_by('-end_date').first()
        
        if existing_package:
            UserPackage.objects.filter(id=existing_package.id).update(
                end_date=self.end_date,
                posts_per_month=self.posts_per_month,
                credits=self.credits
            )
        else:
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.package_type}"