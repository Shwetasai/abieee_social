'''from django.db import models
from django.contrib.auth.models import User
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
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="business_questionnaire")
    core_business_values = models.TextField(blank=False, null=False)
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
    image_type_preferences = models.TextField(max_length=255, choices=IMAGE_TYPE_CHOICES, blank=False, null=False)
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
        return f"{self.business.business_name}"'''

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
    logo = models.ImageField(upload_to="uploads/logos/", null=True, blank=True)
    
  
    BUSINESS_VOICE_CHOICES = [
        ("personal and authentic", "Personal and Authentic"),
        ("professional and expert", "Professional and Expert"),
        ("formal and corporate", "Formal and Corporate"),
        ("friendly and approachable", "Friendly and Approachable"),
        ("creative and innovative", "Creative and Innovative"),
        ("authoritative and expert", "Authoritative and Expert"),
        ("simple and clear", "Simple and Clear"),
        ("reliable and trustworthy", "Reliable and Trustworthy"),
        ("pleasant and positive", "Pleasant and Positive"),
        ("encouraging and supportive", "Encouraging and Supportive"),
        ("inspirational and motivating", "Inspirational and Motivating"),
        ("informative and educational", "Informative and Educational"),
        ("focused and goal-oriented", "Focused and Goal-Oriented"),
        ("positive and uplifting", "Positive and Uplifting"),
        ("others", "Others"),
    ]
    GEOGRAPHIC_AREA_CHOICES = [
        ("israel_only", "Israel only"),
        ("israel_and_international", "Israel and international activity"),
        ("international_only", "International activity only"),
    ]
    BUSINESS_SIZE_CHOICES = [
        ("1-10", "1-10 Employees"),
        ("11-50", "11-50 Employees"),
        ("51-200", "51-200 Employees"),
        ("201-500", "201-500 Employees"),
        ("501-1000", "501-1000 Employees"),
        ("1000+", "1000+ Employees"),
    ]
    CONTENT_PREFERENCE_CHOICES = [
        ("Professional Tips", "Professional Tips"),
        ("Industry Insights", "Industry Insights"),
        ("Personal Thoughts", "Personal Thoughts"),
        ("Success Stories", "Success Stories"),
        ("Inspirational Content", "Inspirational Content"),
        ("How-to Guides", "How-to Guides"),
        ("Educational Content", "Educational Content"),
        ("In-depth Analysis", "In-depth Analysis"),
        ("Company Updates", "Company Updates"),
        ("Product/Services Reviews", "Product/Services Reviews"),
        ("Behind the Scenes", "Behind the Scenes"),
        ("Case Studies", "Case Studies"),
        ("Industry News", "Industry News"),
        ("Engagement Questions", "Engagement Questions"),
        ("Other", "Other"),
    ]
    CONTENT_TO_AVOID_CHOICES = [
        ("Overly Commercial Content", "Overly Commercial Content"),
        ("Aggressive Sales Posts", "Aggressive Sales Posts"),
        ("Generic Content", "Generic Content"),
        ("other", "Other"),
    ]
    POSTING_FREQUENCY_CHOICES = [
        ("once_a_month", "Once_a_month"),
        ("twice_a_month", "Twice_a_month"),
        ("once_a_week", "Once_a_week"),
        ("2-3_times_in_a_week", "2-3_times_in_a_week"),
        ("4-5_times_a_week","4-5_times_a_week")
    ]
    LINKEDIN_CONTENT_CHOICES = [
        ("in_depth_articles", "In-depth professional articles"),
        ("customer_success", "Customer success stories"),
        ("professional_dilemmas", "Professional dilemmas and their solutions"),
        ("insights_meetings", "Insights from professional meetings"),
        ("case_study", "Case study analysis"),
        ("sharing_tools", "Sharing professional tools"),
        ("sharing_challenges", "Sharing professional challenges"),
        ("industry_insights", "Industry insights"),
        ("professional_tips", "Professional tips"),
        ("innovation", "Innovation in the field"),
        ("work_process", "A glimpse into work processes"),
        ("future_predictions", "Future predictions in the field"),
        ("new_tech_explanations", "Explanations about new technologies"),
        ("faq_answers", "Answering frequently asked questions in the field"),
        ("market_trend", "Market trend analysis"),
        ("learning_sharing", "Sharing in learning processes"),
        ("business_decision_sharing", "Sharing in business decisions"),
        ("book_recommendations", "Sharing recommended books/articles"),
        ("discussion_questions", "Professional questions for discussion"),
        ("study_summaries", "Summaries of relevant studies"),
        ("other", "Other"),
    ]

    FACEBOOK_CONTENT_CHOICES = [
        ("personal_stories", "Personal stories"),
        ("educational_content", "Educational content"),
        ("customer_stories", "Customer stories"),
        ("insights_field", "Insights from the field"),
        ("interesting_news", "Interesting news in the field"),
        ("behind_scenes", "Behind the scenes"),
        ("inspirational_stories", "Inspirational stories"),
        ("tips_recommendations", "Tips and recommendations"),
        ("regular_updates", "Regular updates"),
        ("questions_surveys", "Questions and surveys"),
        ("funny_field_posts", "Funny posts from the field"),
        ("thought_provoking_posts", "Thought-provoking posts"),
        ("decision_making", "Participation in decision-making processes"),
        ("customer_feedback", "Sharing customer feedback"),
        ("sharing_experiences", "Sharing experiences"),
        ("getting_to_know_team", "Getting to know the team"),
        ("special_events", "Special events"),
        ("sharing_deliberations", "Sharing in deliberations"),
        ("special_value_offers", "Special value offers"),
        ("product_testing", "Tastings of new products/services"),
        ("other", "Other"),
    ]

    INSTAGRAM_CONTENT_CHOICES = [
        ("behind_scenes_photos", "Behind the scenes photos"),
        ("visual_results_projects", "Visual results of projects"),
        ("short_tutorial_videos", "Short tutorial videos"),
        ("amusing_office_moments", "Amusing moments from the office/work"),
        ("professional_event_photos", "Photos from professional events"),
        ("sharing_business_hobbies", "Sharing business-related hobbies"),
        ("sharing_sources_inspiration", "Sharing sources of inspiration"),
        ("photo_tips", "Photo tips"),
        ("work_process_photos", "Work process photographs"),
        ("inspirational_quotes", "Inspirational Quotes"),
        ("introducing_team", "Introducing the team"),
        ("office_work_tours", "Office/workshop tours"),
        ("eureka_moments", '"Eureka" moments'),
        ("visual_challenges", "Visual challenges"),
        ("daily_moments_inspiration", "Daily moments of inspiration"),
        ("meetings_customers", "Meetings with customers"),
        ("before_after_photos", '"Before-after" photos'),
        ("celebrating_successes", "Celebrating small successes"),
        ("visual_trends_field", "Visual trends in the field"),
        ("pictures_tools", "Pictures of tools"),
        ("other", "Other"),
    ]

    TIKTOK_CONTENT_CHOICES = [
        ("quick_tips", "Quick Tips"),
        ("short_quick_demos", "Short and quick demos"),
        ("time_lapse_workflows", "Time-lapse workflows"),
        ("behind_scenes_funny", "Behind the scenes funny"),
        ("faq_answers", "Answers to frequently asked questions"),
        ("trends_field", "Trends in the field"),
        ("day_in_life", '"A day in the life" of the business'),
        ("professional_tricks", "Professional tricks"),
        ("fast_paced_success_stories", "Fast-paced success stories"),
        ("short_interesting_explanations", "Short and interesting explanations"),
        ("responses_popular_trends", "Responses to popular trends"),
        ("sharing_mistakes_lessons", "Sharing mistakes and lessons learned"),
        ("duets_relevant_content", "Duets with relevant content"),
        ("short_series_tips", "Short series of tips"),
        ("moving_products_services", "Moving on to products/services"),
        ("creative_customer_responses", "Creative customer responses"),
        ("professional_challenges", "Professional challenges"),
        ("quick_before_after_demos", 'Quick "before-after" demos'),
        ("sharing_technological_innovation", "Sharing in technological innovation"),
        ("amusing_moments_work", "Amusing moments from work"),
        ("other", "Other"),
    ]
    PERSONAL_BUSINESS_STORY_CHOICES=[
        ("how_it_started", "How it all started"),
        ("moment_changed_attitude", "Moment that changed attitude"),
        ("serious_challenge", "Serious challenge faced"),
        ("unique_inspiration", "Unique source of inspiration"),
        ("goal_reflected_values", "Goal reflecting values"),
        ("open_for_free_filling", "Open for free filling"),
    ]
    BUSINESS_TOP_VALUES_CHOICES=[
        ("innovation", "Innovation"),
        ("reliability", "Reliability"),
        ("transparency", "Transparency"),
        ("professionalism", "Professionalism"),
        ("community", "Community"),
        ("environmental", "Environmental"),
        ("accountability", "Accountability"),
        ("creativity", "Creativity"),
        ("tradition", "Tradition"),
        ("other", "Other"),
    ]
    PERSONAL_TWIST_CHOICES = [
        ("unique_professional_background", "Unique professional background"),
        ("hobby_integrates_business", "A hobby that integrates into a business"),
        ("unconventional_approach", "An unconventional approach"),
        ("surprising_combination_fields", "A surprising combination of fields"),
        ("other", "Other"),
    ]
    BEHIND_BRAND_STORY_CHOICES = [
        ("unique_work_processes", "Unique work processes"),
        ("special_traditions", "Special traditions in the business"),
        ("interesting_anecdotes", "Interesting anecdotes"),
        ("daily_rituals", "Daily rituals"),
        ("other", "Other"),
    ]
    COMMUNICATION_STYLE_CHOICES = [
        ("professional_formal", "Professional-formal"),
        ("sociable_personal", "Sociable-personal"),
        ("mixed_professional_personal", "Mixed - Professional with a personal touch"),
        ("humoristic", "Humoristic"),
        ("educational_guide", "Educational-Guide"),
    ]

    COMMUNICATION_PREFERENCE_CHOICES = [
        ("first_person_singular", "First person singular"),
        ("first_person_plural", "First person plural"),
        ("company_name", "Company name"),
        ("combination", "Combination"),
    ]

    BUSINESS_DESCRIPTION_CHOICES = [
        ("professional", "Professional"),
        ("reliable", "Reliable"),
        ("innovative", "Innovative"),
        ("creative", "Creative"),
        ("caring", "Caring"),
        ("qualitative", "Qualitative"),
        ("accessible", "Accessible"),
        ("advanced", "Advanced"),
        ("traditional", "Traditional"),
        ("prestigious", "Prestigious"),
        ("friendly", "Friendly"),
        ("precise", "Precise"),
        ("flexible", "Flexible"),
        ("fast", "Fast"),
        ("sociable", "Sociable"),
        ("other", "Other"),
    ]

    BUSINESS_EXPLANATION_CHOICES = [
        ("professional_formal", "Professional and formal"),
        ("friendly_personal", "Friendly and personal"),
        ("mixed", "Mixed"),
        ("humorous_lighthearted", "Humorous and light-hearted"),
        ("educational_explanatory", "Educational and explanatory"),
        ("storytelling_inspiring", "Storytelling and inspiring"),
        ("other", "Other"),
    ]

    PLATFORM_CHOICES = [
        ("facebook", "Facebook"),
        ("instagram", "Instagram"),
        ("linkedin", "LinkedIn"),
        ("tiktok", "TikTok"),
        ("twitter_x", "Twitter/X"),
        ("youtube", "YouTube"),
        ("other", "Other"),
    ]

    MEDIA_CHOICES = [
        ("professional_photos", "Professional photos"),
        ("authentic_photos_field", "Authentic photos from the field"),
        ("short_videos", "Short videos"),
        ("long_videos", "Long videos"),
        ("presentations_carousels", "Presentations/Carousels"),
        ("infographics", "Infographics"),
        ("reels_stories", "Reels/Stories"),
        ("lives", "Lives"),
        ("other", "Other"),
    ]

    GOAL_CHOICES = [
        ("increase_brand_awareness", "Increase brand awareness"),
        ("attract_new_customers", "Attract new customers"),
        ("build_professional_trust", "Build professional trust"),
        ("educate_market", "Educate the market"),
        ("create_community", "Create a community"),
        ("increase_sales", "Increase sales"),
        ("share_professional_knowledge", "Share professional knowledge"),
        ("show_people_behind_business", "Show the people behind the business"),
        ("other", "Other"),
    ]
    BRAND_PERSONALITY_CHOICES=[
        ("professional","Professional"),
        ("Innovative","Innovative"),
        ("traditional","traditional"),
        ("young","young"),
        ("reliable","reliable"),
        ("creative","creative"),
        ("dynamic","dynamic"),
        ("prestigious","prestigious"),
        ("friendly","friendly"),
        ("other","other")
    ]
    CONTENT_ATMOSPERE_CHOICES=[
        ("Professional_serious","Professional and serious"),
        ("Light_fun","Light and fun"),
        ("Warm_personal","Warm and personal"),
        ("Inspiring","Inspiring"),
        ("Educational_teaching","Educational and teaching"),
        ("Innovative_advanced","Innovative and advanced"),
        ("Elegant_luxurious","Elegant and luxurious"),
        ("Young_dynamic","Young and dynamic"),
        ("other","other")
    ]
    POST_SOUNDS_CHOICES=[
        ("conversation_with_friend","Like a conversation with a friend"),
        ("professional_lecture","Like a professional lecture"),
        ("tips_from_expert","Like tips from the expert"),
        ("interesting_story","Like an interesting story"),
        ("practical_guide","Like a practical guide"),
        ("other","Other")
    ]
    LINGUISTIC_STYLE_CHOICES=[
        ("High-level_professional_language","High-level and professional language"),
        ("Simple_accessible_language","Simple and accessible language"),
        ("young_contemporary_language","Young and contemporary language"),
        ("warm_personal_language","Warm and personal language"),
        ("Combination_of","combination of")
    ]
    PHOTO_STYLE_CHOICES=[
        ("Realistic_professional","Realistic and professional"),
        ("Painted_artistic","Painted and artistic"),
        ("Minimalist_clean","Minimalist and clean"),
        ("Colorful_vibrant","Colorful and vibrant"),
        ("Soft_delicate","Soft and delicate"),
        ("Digital_modern","Digital and modern"),
        ("Vintage_classic","Vintage and classic"),
        ("Other","other")
    ]
    FAVORITE_COLORS_CHOICES=[
        ("Warm colors","Warm_colors"),
        ("Cold colors","Cold_colors"),
        ("Monochromatic","monochromatic"),
        ("Brand colors only","Brand_colors_only"),
        ("Pastels","pastels"),
        ("Bright colors","Bright_colors"),
        ("Other","other")
    ]
    PHOTOS_CONVEY_CHOICES=[
        ("Professional and business","Professional_business"),
        ("Warm and homely","Warm_homely"),
        ("Young and dynamic","Young_dynamic"),
        ("Luxurious and elegant","Luxurious_elegant"),
        ("Natural and authentic","Natural_authentic"),
        ("Innovative and technological","Innovative_technological"),
        ("Other","other")
    ]
    BRAND_COLOURS_CHOICES = [
        ("secondary_1", "1st Secondary Color"),
        ("secondary_2", "2nd Secondary Color"),
        ("secondary_3", "3rd Secondary Color"),
        ("secondary_4", "4th Secondary Color"),
        ("secondary_5", "5th Secondary Color"),
    ]
    SUCCESS_METRICS_CHOICES=[
        ("Likes_comments","Likes and comments"),
        ("Shares","shares"),
        ("Links","links"),
        ("Reading_time","reading time"),
        ("Conversions_sales","conversions and sales"),
        ("Growth_followers","growth in followers"),
        ("Website_traffic","website traffic"),
        ("New_inquiries","new inquiries"),
        ("Brand_memories","Brand memories"),
        ("Other","other")
    ]
    FORMALITY_CHOICES=[
        ("Very informal","Very_informal"),
        ("Informal","informal"),
        ("Medium","medium"),
        ("Formal","formal"),
        ("Very formal","Very_formal")
    ]

    
    def __str__(self):
        return self.user.email
