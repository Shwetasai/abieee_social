from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
class BusinessDetails(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="business_profile")
    business_name = models.CharField(max_length=255)
    field_of_activity = models.CharField(max_length=255)
    business_description = models.TextField()
    target_audience = models.TextField()
    business_identity = models.TextField()

    SOCIAL_MEDIA_CHOICES = [
        ('facebook', 'Facebook'),
        ('twitter', 'Twitter'),
        ('instagram', 'Instagram'),
        ('linkedin', 'LinkedIn'),
        ('others', 'Others'),
    ]
    social_media_presence = models.CharField(
        max_length=15,
        choices=SOCIAL_MEDIA_CHOICES,
        default='others'
    )
    social_media_link = models.URLField(blank=True, null=True)

    goals_and_challenges = models.TextField(
        help_text=(
            "1. What are your main goals on social media?\n"
            "2. What are the main challenges you are facing today?"
        )
    )
    current_management = models.TextField(
        help_text=(
            "1. How do you manage social networks today?\n"
            "2. How much time do you spend on average on social media management per month?\n"
            "3. Where did you hear about us?"
        )
    )
    
    def __str__(self):
        return f" {self.business_name}"


class BusinessProfileQuestionnaire(models.Model):
    business = models.OneToOneField(BusinessDetails, on_delete=models.CASCADE, related_name="questionnaire")
    core_business_values = models.TextField(max_length=500, blank=False, null=False)
    unique_selling_proposition = models.TextField(max_length=500, blank=False, null=False)

    BUSINESS_VOICE_CHOICES = [('professional', 'Professional'), ('friendly', 'Friendly'), ('formal', 'Formal'), ('casual', 'Casual'), ('innovative', 'Innovative'), ('other', 'Other')]
    business_voice = models.CharField(max_length=20, choices=BUSINESS_VOICE_CHOICES, default='professional', blank=False, null=False)
    business_voice_other = models.TextField(max_length=255, blank=True, null=True)

    main_customers = models.TextField(max_length=255, blank=False, null=False)
    customers_language = models.CharField(max_length=500, blank=False, null=False)
    main_challenges = models.TextField(max_length=500, blank=False, null=False)
    business_challenges_solution = models.TextField(max_length=500, blank=True, null=True)

    COMMUNICATION_TONE_CHOICES = [('formal', 'Formal'), ('casual', 'Casual'), ('professional', 'Professional'), ('friendly', 'Friendly')]
    communication_tone = models.CharField(max_length=15, choices=COMMUNICATION_TONE_CHOICES, default='formal', blank=False, null=False)

    EMOJI_USAGE_CHOICES = [('frequent', 'Frequent'), ('moderate', 'Moderate'), ('minimal', 'Minimal')]
    emoji_usage = models.CharField(max_length=10, choices=EMOJI_USAGE_CHOICES, default='moderate', blank=False, null=False)

    important_phrases = models.TextField(blank=False, null=False)
    phrases_avoid = models.TextField(blank=False, null=False)

    WRITING_STYLE_CHOICES = [('concise', 'Short and concise sentences'), ('detailed', 'Detailed explanations'), ('technical', 'Use of technical terms'), ('conversational', 'Conversational style')]
    writing_style = models.CharField(max_length=15, choices=WRITING_STYLE_CHOICES, default='concise', blank=False, null=False)
    additional_communication_preferences = models.TextField(blank=True, null=True)

    content_type_preference = models.CharField(max_length=255, blank=False, null=False)
    educational_content_percentage = models.PositiveIntegerField(blank=False, null=False,default=0)
    promotional_content_percentage = models.PositiveIntegerField(blank=False, null=False,default=0)
    behind_the_scenes_percentage = models.PositiveIntegerField(blank=False, null=False,default=0)
    inspirational_content_percentage = models.PositiveIntegerField(blank=False, null=False,default=0)
    seasonal_content_description = models.TextField(blank=True, null=True)

    BRAND_COLORS = [('#primary_color', 'Primary Color'), ('#secondary_color', 'Secondary Color'), ('#accent_color', 'Accent Color')]
    primary_color = models.CharField(max_length=16, choices=BRAND_COLORS, default='#primary_color', blank=False, null=False)
    secondary_color = models.CharField(max_length=16, choices=BRAND_COLORS, default='#secondary_color', blank=False, null=False)
    accent_color = models.CharField(max_length=16, choices=BRAND_COLORS, default='#accent_color', blank=False, null=False)

    VISUAL_STYLE_CHOICES = [('minimalist', 'Minimalist'), ('rich_and_detailed', 'Rich and Detailed'), ('modern', 'Modern'), ('classic', 'Classic')]
    preferred_visual_style = models.CharField(max_length=50, choices=VISUAL_STYLE_CHOICES, blank=False, null=False)

    IMAGE_TYPE_CHOICES = [('product_photos', 'Product Photos'), ('lifestyle_photos', 'Lifestyle Photos'), ('illustrations', 'Illustrations'), ('infographics', 'Infographics')]
    image_type_preferences = models.CharField(max_length=255, choices=IMAGE_TYPE_CHOICES, blank=False, null=False)
    additional_design_notes = models.TextField(blank=True, null=True)
    successful_post_examples = models.TextField(blank=False, null=False)
    inspiring_brands = models.TextField(blank=False, null=False)
    most_successful_post = models.TextField(blank=False, null=False)
    made_successful = models.TextField(blank=False, null=False)

    successful_post_definition = models.TextField(blank=False, null=False)
    BUSINESS_GOAL_CHOICES = [('brand_awareness', 'Increase Brand Awareness'), ('drive_sales', 'Drive Sales'), ('customer_loyalty', 'Build Customer Loyalty'), ('increase_engagement', 'Increase Engagement')]
    business_goals = models.CharField(max_length=255, choices=BUSINESS_GOAL_CHOICES, blank=False, null=False)
    topics_to_avoid = models.TextField(blank=False, null=False)
    additional_guidelines = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.business_name}"
