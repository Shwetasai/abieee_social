from django.db import models
import uuid
from prices.models import Package
from django.conf import settings

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