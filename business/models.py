from django.db import models

class BusinessDetails(models.Model):
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
        return self.business_name


class BusinessProfileQuestionnaire(models.Model):
    BUSINESS_VOICE_CHOICES = [
        ('professional', 'Professional'),
        ('friendly', 'Friendly'),
        ('formal', 'Formal'),
        ('casual', 'Casual'),
        ('innovative', 'Innovative'),
        ('other', 'Other'),
    ]

    business = models.OneToOneField(BusinessDetails, on_delete=models.CASCADE, primary_key=True)
    core_business_values = models.TextField(max_length=500,blank=False, null=False)
    unique_selling_proposition = models.TextField(max_length=500,blank=False, null=False)
    business_voice = models.CharField(
        max_length=20,
        choices=BUSINESS_VOICE_CHOICES,
        default='professional'
    )
    business_voice_other = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    """current_step = models.PositiveIntegerField(default=2)
    completed_percentage = models.PositiveIntegerField(default=14)"""

    def __str__(self):
        return f"Questionnaire for {self.business.business_name}"

class CommunicationPreferences(models.Model):
    COMMUNICATION_TONE_CHOICES = [
        ('formal', 'Formal'),
        ('casual', 'Casual'),
        ('professional', 'Professional'),
        ('friendly', 'Friendly'),
    ]
    
    EMOJI_USAGE_CHOICES = [
        ('frequent', 'Frequent'),
        ('moderate', 'Moderate'),
        ('minimal', 'Minimal'),
    ]
    main_customers=models.TextField(max_length=255,blank=False, null=False)
    customers_language=models.CharField(max_length=500,blank=False, null=False)
    main_challenges=models.TextField(max_length=500,blank=False, null=False)
    business_challenges_solution = models.TextField(max_length=500,blank=False, null=False)
    communication_tone = models.CharField(blank=False, null=False,
        max_length=15, 
        choices=COMMUNICATION_TONE_CHOICES,default='formal'
    )
    emoji_usage = models.CharField(
        max_length=10, 
        choices=EMOJI_USAGE_CHOICES,default='moderate'
    )
    """current_step = models.PositiveIntegerField(default=3)
    completed_percentage = models.PositiveIntegerField(default=29)"""

    def __str__(self):
        return f"Tone: {self.communication_tone}, Emoji: {self.emoji_usage}"

class CommunicationStyle(models.Model):
    WRITING_STYLE_CHOICES = [
        ('concise', 'Short and concise sentences'),
        ('detailed', 'Detailed explanations'),
        ('technical', 'Use of technical terms'),
        ('conversational', 'Conversational style'),
    ]
    important_phrases=models.TextField()
    phrases_avoid=models.TextField()
    writing_style=models.CharField(
    blank=False, 
    null=False,
    max_length=15,
    choices=WRITING_STYLE_CHOICES,default='concise')
    additional_communication_preferences = models.TextField(blank=True, null=True)
    """current_step = models.PositiveIntegerField(default=4)
    completed_percentage = models.PositiveIntegerField(default=43)"""

    def __str__(self):
        return f"Writing Style: {self.writing_style}"

class ContentTypes(models.Model):
    content_type_preference = models.CharField(max_length=255, blank=True, null=True)
    educational_content_percentage = models.PositiveIntegerField(blank=False, null=False)
    promotional_content_percentage = models.PositiveIntegerField(blank=False, null=False)
    behind_the_scenes_percentage = models.PositiveIntegerField(blank=False, null=False)
    inspirational_content_percentage = models.PositiveIntegerField(blank=False, null=False)
    seasonal_content_description = models.TextField(blank=True, null=True)
    """current_step = models.PositiveIntegerField(default=4)
    completed_percentage = models.PositiveIntegerField(default=57)"""

    def __str__(self):
        return f"Content Preference: {self.content_type_preference}"



class VisualStyle(models.Model):
    BRAND_COLORS = [
        ('#primary_color', 'Primary Color'),
        ('#secondary_color', 'Secondary Color'),
        ('#accent_color', 'Accent Color'),
    ]

    primary_color = models.CharField(
        max_length=16,
        choices=BRAND_COLORS,
        default='#primary_color'
    )
    secondary_color = models.CharField(
        max_length=16,
        choices=BRAND_COLORS,
        default='#secondary_color'
    )
    accent_color = models.CharField(
        max_length=16,
        choices=BRAND_COLORS,
        default='#accent_color'
    )

    VISUAL_STYLE_CHOICES = [
        ('minimalist', 'Minimalist'),
        ('rich_and_detailed', 'Rich and Detailed'),
        ('modern', 'Modern'),
        ('classic', 'Classic'),
    ]
    preferred_visual_style = models.CharField(
        max_length=50,
        choices=VISUAL_STYLE_CHOICES,
        blank=False,
        null=False,
    )

    IMAGE_TYPE_CHOICES = [
        ('product_photos', 'Product Photos'),
        ('lifestyle_photos', 'Lifestyle Photos'),
        ('illustrations', 'Illustrations'),
        ('infographics', 'Infographics'),
    ]

    image_type_preferences = models.CharField( 
        max_length=255,
        choices=IMAGE_TYPE_CHOICES,
        blank=False,
        null=False,
    )
    additional_design_notes = models.TextField(blank=True, null=True)
    successful_post_examples = models.TextField(blank=True, null=True)
    inspiring_brands = models.TextField(blank=True, null=True)
    most_successful_post = models.TextField(blank=True, null=True)
    made_successful=models.TextField(blank=True, null=True)
    """current_step = models.PositiveIntegerField(default=5)
    completed_percentage = models.PositiveIntegerField(default=71)"""

    def __str__(self):
        return f"Visual Style: {self.preferred_visual_style}"

class SuccessMetrics(models.Model):
    successful_post_definition = models.TextField(blank=False, null=False)

    BUSINESS_GOAL_CHOICES = [
        ('brand_awareness', 'Increase Brand Awareness'),
        ('drive_sales', 'Drive Sales'),
        ('customer_loyalty', 'Build Customer Loyalty'),
        ('increase_engagement', 'Increase Engagement'),
    ]

    business_goals = models.CharField(
        max_length=255,
        choices=BUSINESS_GOAL_CHOICES,
        blank=False,
        null=False,
    )
    topics_to_avoid = models.TextField(blank=True, null=True)
    additional_guidelines = models.TextField(blank=True, null=True)
    """current_step = models.PositiveIntegerField(default=6)
    completed_percentage = models.PositiveIntegerField(default=100)"""
    def __str__(self):
        return f"Business Goal: {self.business_goals}"