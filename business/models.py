from django.db import models
from django.conf import settings

class BusinessDetails(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="business_profile")
    business_name = models.CharField(max_length=255)
    field_of_activity = models.CharField(max_length=255)
    business_description = models.TextField()
    target_audience = models.TextField()
    social_media = models.JSONField(default=dict) 
    business_goals = models.JSONField(default=dict) 
    business_challenges  = models.JSONField(default=dict) 
    current_management = models.JSONField(default=dict) 

    def __str__(self):
        return self.business_name

class BusinessProfileQuestionnaire(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="business_questionnaire")
    business_data = models.JSONField(default=dict) 


    
  
