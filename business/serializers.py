'''from rest_framework import serializers
from business.models import (BusinessDetails, BusinessProfileQuestionnaire)
class BusinessDetailsSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')
    class Meta:
        model = BusinessDetails
        fields = ['id', 'business_name', 'field_of_activity', 'business_description', 'target_audience', 
                  'social_media_presence', 'social_media_link', 'goals_and_challenges', 'current_management','user']

class BusinessProfileQuestionnaireSerializer(serializers.ModelSerializer):
    page_num = serializers.IntegerField(write_only=True, required=False)  

    class Meta:
        model = BusinessProfileQuestionnaire
        fields = '__all__'

    def to_internal_value(self, data):
        page_num = data.get('page_num')

        if page_num is not None:
            try:
                page_num = int(page_num)
            except ValueError:
                raise serializers.ValidationError({"page_num": "Invalid page number."})
            page_fields = {
                1: ['core_business_values', 'unique_selling_proposition', 'business_voice'],
                2: ['main_customers', 'customers_language', 'main_challenges'],
                3: ['important_phrases', 'phrases_avoid'],
                4: ['content_type_preference'],
                5: ['preferred_visual_style', 'image_type_preferences'],
                6: ['successful_post_examples', 'inspiring_brands'],
                7: ['successful_post_definition', 'business_goals', 'topics_to_avoid']
            }

            required_fields = page_fields.get(page_num, [])

            validated_data = {field: data[field] for field in required_fields if field in data}

            if len(validated_data) != len(required_fields):
                missing_fields = [field for field in required_fields if field not in data]
                raise serializers.ValidationError({
                "message": f"Page {page_num} data validation failed.",
                "errors": {field: "This field is required." for field in missing_fields}
                })

            return validated_data
        return super().to_internal_value(data)

'''

from rest_framework import serializers
from .models import BusinessDetails, BusinessProfileQuestionnaire
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

class BusinessDetailsSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = BusinessDetails
        fields = '__all__'

class BusinessProfileQuestionnaireSerializer(serializers.ModelSerializer):
    page_num = serializers.IntegerField(write_only=True, required=False)
    logo = serializers.ImageField(required=False, validators=[
        FileExtensionValidator(allowed_extensions=["png", "jpg", "jpeg", "svg"])])

    class Meta:
        model = BusinessProfileQuestionnaire
        fields = '__all__'

    PAGE_FIELDS = {
        1: ["business_size", "years_of_activity", "business_voice", "geographic_area_operation"],
        2: ["content_preference", "content_to_avoid", "main_issues", "main_goals"],
        3: ["linkedin_content", "facebook_content", "instagram_content", "tiktok_content",
            "linkedin_posting_frequency", "facebook_posting_frequency", "instagram_posting_frequency", "tiktok_posting_frequency",
            "global_posting_frequency"],
        4: ["personal_business_story", "business_top_values", "personal_twist", "behind_brand_story","unique_approach","special_method"
          ,"unique_experience","special_strength","get_up_morning","job_things","vision","believes","most_special","name_of_business"
          ,"surprised"],
        5: [ "communication_style", "preferred_words", "avoided_words","business_explanation_style","communication_preferences",
            "communication_perspective","media_types","platforms","content_goals"],
        6: ["core_value","market_uniqueness","brand_personality","business_starting_story","business_vision","content_atmosphere"
        ,"post_sounds","business_keywords","linguistic_style","photos_convey"],
        7: ["avoided_content","sensitive_issue","key_messages","brand_story_sentence","success_metrics","content_distribution"
        ,"tone_examples","formality_level"],
    }

    def validate(self, attrs):
        page_num = attrs.get("page_num")
        business_data = attrs.get("business_data", {})
        errors = {}

        if page_num in self.PAGE_FIELDS:
            missing_fields = [field for field in self.PAGE_FIELDS[page_num] if field not in business_data or not business_data[field]]
            if missing_fields:
                errors.update({field: "This field is required and cannot be empty." for field in missing_fields})
        if page_num == 1:
            business_size = business_data.get("business_size")
            valid_business_sizes = [choice[0] for choice in BusinessProfileQuestionnaire.BUSINESS_SIZE_CHOICES]
            if business_size and business_size not in valid_business_sizes:
                errors["business_size"] = f"Invalid choice. Choose from {valid_business_sizes}."

            geographic_area_operation = business_data.get("geographic_area_operation")
            valid_geo_areas = [choice[0] for choice in BusinessProfileQuestionnaire.GEOGRAPHIC_AREA_CHOICES]
            if geographic_area_operation and geographic_area_operation not in valid_geo_areas:
                errors["geographic_area_operation"] = f"Invalid choice. Choose from {valid_geo_areas}."

            years_of_activity = business_data.get("years_of_activity")
            if years_of_activity is not None and not isinstance(years_of_activity, int):
                errors["years_of_activity"] = "This field must be an integer."

        if page_num == 2:
            content_preference = business_data.get("content_preference", [])
            valid_content_choices = [choice[0] for choice in BusinessProfileQuestionnaire.CONTENT_PREFERENCE_CHOICES]
            if not isinstance(content_preference, list):
                errors["content_preference"] = "Must be a list of choices."
            if not (3 <= len(content_preference) <= 5):
                errors["content_preference"] = "You must select between 3 and 5 content preferences."
            invalid_choices = [choice for choice in content_preference if choice.lower() not in [vc.lower() for vc in valid_content_choices]]
            if invalid_choices:
                errors["content_preference"] = f"Invalid choices: {invalid_choices}. Choose from {valid_content_choices}."

            main_issues = business_data.get("main_issues", "").strip()
            if len(main_issues) > 1000:
                errors["main_issues"] = "Maximum length exceeded (1000 characters allowed)."

            main_goals = business_data.get("main_goals", "").strip()
            if len(main_goals) > 1000:
                errors["main_goals"] = "Maximum length exceeded (1000 characters allowed)."

            content_to_avoid = business_data.get("content_to_avoid")
            valid_content_to_avoid_choices = [choice[0] for choice in BusinessProfileQuestionnaire.CONTENT_TO_AVOID_CHOICES]
            if content_to_avoid and content_to_avoid.lower() not in [choice.lower() for choice in valid_content_to_avoid_choices]:
                errors["content_to_avoid"] = f"Invalid choice: {content_to_avoid}. Choose from {valid_content_to_avoid_choices}."

        if page_num == 3:
            valid_choices = {
                "linkedin_content": [choice[0] for choice in BusinessProfileQuestionnaire.LINKEDIN_CONTENT_CHOICES],
                "facebook_content": [choice[0] for choice in BusinessProfileQuestionnaire.FACEBOOK_CONTENT_CHOICES],
                "instagram_content": [choice[0] for choice in BusinessProfileQuestionnaire.INSTAGRAM_CONTENT_CHOICES],
                "tiktok_content": [choice[0] for choice in BusinessProfileQuestionnaire.TIKTOK_CONTENT_CHOICES],
            }
            for field, valid_list in valid_choices.items():
                content = business_data.get(field, [])
                if not isinstance(content, list):
                    errors[field] = "Invalid data type. Must be a list."
                else:
                    invalid_choices = [choice for choice in content if choice not in valid_list]
                    if invalid_choices:
                        errors[field] = f"Invalid choices: {invalid_choices}. Choose from {valid_list}."

            valid_posting_frequencies = [choice[0] for choice in BusinessProfileQuestionnaire.POSTING_FREQUENCY_CHOICES]
            posting_frequency_fields = [
                "linkedin_posting_frequency", "facebook_posting_frequency", "instagram_posting_frequency",
                "tiktok_posting_frequency", "global_posting_frequency"]
            for field in posting_frequency_fields:
                value = business_data.get(field)
                if value and value not in valid_posting_frequencies:
                    errors[field] = f"Invalid posting frequency: {value}. Choose from {valid_posting_frequencies}."

        if page_num == 4:
            personal_business_story = business_data.get("personal_business_story", [])
            valid_story_choices = [choice[0] for choice in BusinessProfileQuestionnaire.PERSONAL_BUSINESS_STORY_CHOICES]
            if not isinstance(personal_business_story, list):
                errors["personal_business_story"] = "Must be a list of selected choices."
            else:
                invalid_choices = [choice for choice in personal_business_story if choice not in valid_story_choices]
                if invalid_choices:
                    errors["personal_business_story"] = f"Invalid choices: {invalid_choices}. Choose from {valid_story_choices}."
                for choice in personal_business_story:
                    input_field = business_data.get(f"personal_business_story_input_{choice}", "").strip()
                    if not input_field:
                        errors[f"personal_business_story_input_{choice}"] = f"Additional information required for '{choice}'."

            personal_twist = business_data.get("personal_twist", [])
            valid_twist_choices  = [choice[0] for choice in BusinessProfileQuestionnaire.PERSONAL_TWIST_CHOICES]
            if not isinstance(personal_twist, list):
                errors["personal_twist"] = "Must be a list of selected choices."
            else:
                invalid_choices = [choice for choice in personal_twist if choice not in valid_twist_choices]
                if invalid_choices:
                    errors["personal_twist"] = f"Invalid choices: {invalid_choices}. Choose from {valid_twist_choices}."
                for choice in personal_twist:
                    input_field = business_data.get(f"personal_twist_input_{choice}", "").strip()
                    if not input_field:
                        errors[f"personal_twist_input_{choice}"] = f"Additional information required for '{choice}'."

            behind_brand_story = business_data.get("behind_brand_story", [])
            valid_story_choices = [choice[0] for choice in BusinessProfileQuestionnaire.BEHIND_BRAND_STORY_CHOICES]
            if not isinstance(behind_brand_story, list):
                errors["behind_brand_story"] = "Must be a list of selected choices."
            else:
                invalid_choices = [choice for choice in behind_brand_story if choice not in valid_story_choices]
                if invalid_choices:
                    errors["behind_brand_story"] = f"Invalid choices: {invalid_choices}. Choose from {valid_story_choices}."
                for choice in behind_brand_story:
                    input_field = business_data.get(f"behind_brand_story_input_{choice}", "").strip()
                    if not input_field:
                        errors[f"behind_brand_story_input_{choice}"] = f"Additional information required for '{choice}'."
            if "other" in behind_brand_story:
                custom_story = business_data.get("custom_behind_brand_story", "").strip()
                if not custom_story:
                    errors["custom_behind_brand_story"] = "This field is required when 'other' is selected."

            business_top_values = business_data.get("business_top_values", [])
            valid_values = [choice[0] for choice in BusinessProfileQuestionnaire.BUSINESS_TOP_VALUES_CHOICES]
            if not isinstance(business_top_values, list):
                errors["business_top_values"] = "Must be a list of selected choices."
            else:
                if not (1 <= len(business_top_values) <= 3):
                    errors["business_top_values"] = "You must select between 1 and 3 values."
                invalid_choices = [choice for choice in business_top_values if choice not in valid_values]
                if invalid_choices:
                    errors["business_top_values"] = f"Invalid choices: {invalid_choices}. Choose from {valid_values}."
            if "other" in business_top_values:
                custom_value = business_data.get("custom_business_top_value", "").strip()
                if not custom_value:
                    errors["custom_business_top_value"] = "This field is required when 'other' is selected."

        if page_num == 5:
            communication_style = business_data.get("communication_style", "").strip()
            valid_communication_choices = [choice[0] for choice in BusinessProfileQuestionnaire.COMMUNICATION_STYLE_CHOICES]
            if not communication_style:
                errors["communication_style"] = "This field is required and cannot be empty."
            elif communication_style not in valid_communication_choices:
                errors["communication_style"] = f"Invalid choice: {communication_style}. Choose from {valid_communication_choices}."

            preferred_words = business_data.get("preferred_words", "")
            if not isinstance(preferred_words, str):
                errors["preferred_words"] = "Invalid input format."
            
            avoided_words = business_data.get("avoided_words", "")
            if not isinstance(avoided_words, str):
                errors["avoided_words"] = "Invalid input format."

            communication_preferences = business_data.get("communication_preferences", "").strip()
            valid_communication_preferences = {choice[0] for choice in BusinessProfileQuestionnaire.COMMUNICATION_PREFERENCE_CHOICES}
            if not communication_preferences:
                errors["communication_preferences"] = "This field is required and cannot be empty."
            elif communication_preferences not in valid_communication_preferences:
                errors["communication_preferences"] = f"Invalid choice. Choose from {list(valid_communication_preferences)}."

            business_description_words = business_data.get("business_description_words", [])
            valid_description_choices = [choice[0] for choice in BusinessProfileQuestionnaire.BUSINESS_DESCRIPTION_CHOICES]
            if not business_description_words:
                errors["business_description_words"] = "This field is required and cannot be empty."
            elif not isinstance(business_description_words, list):
                errors["business_description_words"] = "Must be a list of selected choices."
            elif len(business_description_words) > 5:
                errors["business_description_words"] = "You can select up to 5 words only."
            else:
                invalid_choices = [choice for choice in business_description_words if choice not in valid_description_choices]
                if invalid_choices:
                    errors["business_description_words"] = f"Invalid choices: {invalid_choices}. Choose from {valid_description_choices}."

            business_explanation_style = business_data.get("business_explanation_style", "").strip()
            valid_explanation_choices = [choice[0] for choice in BusinessProfileQuestionnaire.BUSINESS_EXPLANATION_CHOICES]
            if not business_explanation_style:
                errors["business_explanation_style"] = "This field is required and cannot be empty."
            elif business_explanation_style not in valid_explanation_choices:
                errors["business_explanation_style"] = f"Invalid choice. Choose from {valid_explanation_choices}."

            platforms = business_data.get("platforms", [])
            valid_platforms_choices = [choice[0] for choice in BusinessProfileQuestionnaire.PLATFORM_CHOICES]
            if not isinstance(platforms, list):
                errors["platforms"] = "Must be a list of selected choices."
            else:
                invalid_choices = [choice for choice in platforms if choice not in valid_platforms_choices]
                if invalid_choices:
                    errors["platforms"] = f"Invalid choices: {invalid_choices}. Choose from {valid_platforms_choices}."

            ranking_fields = [
                "professional_experience", "personal_story", "unique_advantages",
                "prices", "service", "quality", "innovation", "other"
            ]
            for field in ranking_fields:
                value = business_data.get(field, None)
                if value is not None:
                    try:
                        value = int(value)
                        if value < 1 or value > 5:
                            errors[field] = "Value must be between 1 and 5."
                    except ValueError:
                        errors[field] = "Invalid input. Must be a number between 1 and 5."

            content_fields = [
                "Professional tips", "Personal stories", "Behind the scenes of the business",
                "Results and successes", "Educational information in the field",
                "Funny content", "Thought-provoking content", "News and updates from the field",
                "Surveys and questions for the audience", "other"
            ]
            for field in content_fields:
                value = business_data.get(field, None)
                if value is not None:
                    try:
                        value = int(value)
                        if value < 1 or value > 5:
                            errors[field] = "Value must be between 1 and 5."
                    except ValueError:
                        errors[field] = "Invalid input. Must be a number between 1 and 5."

            media_types = business_data.get("media_types", [])
            valid_media_choices = [choice[0] for choice in BusinessProfileQuestionnaire.MEDIA_CHOICES]
            if not media_types:
                errors["media_types"] = "This field is required and cannot be empty."
            elif not isinstance(media_types, list):
                errors["media_types"] = "Must be a list of selected choices."
            else:
                invalid_choices = [choice for choice in media_types if choice not in valid_media_choices]
                if invalid_choices:
                    errors["media_types"] = f"Invalid choices: {invalid_choices}. Choose from {valid_media_choices}."

            content_goals = business_data.get("content_goals", [])
            valid_goal_choices = {choice[0] for choice in BusinessProfileQuestionnaire.GOAL_CHOICES}
            if not isinstance(content_goals, list):
                errors["content_goals"] = "Must be a list of selected choices."
            else:
                invalid_choices = [choice for choice in content_goals if choice not in valid_goal_choices]
                if invalid_choices:
                    errors["content_goals"] = f"Invalid choices: {invalid_choices}. Choose from {valid_goal_choices}."
                if len(content_goals) > 3:
                    errors["content_goals"] = "You can select up to 3 goals only."

        if page_num==6:
            core_value= business_data.get("core_value", "")
            if not isinstance(core_value, str):
                errors["core_value"] = "Invalid input format."

            market_uniqueness= business_data.get("market_uniqueness", "")
            if not isinstance(market_uniqueness, str):
                errors["market_uniqueness"] = "Invalid input format."

            business_starting_story = business_data.get("business_starting_story ", "")
            if not isinstance(business_starting_story , str):
                errors["business_starting_story "] = "Invalid input format."

            business_vision= business_data.get("business_vision", "")
            if not isinstance(business_vision, str):
                errors["business_vision"] = "Invalid input format."

            brand_personality= business_data.get("brand_personality", [])
            valid_values = [choice[0] for choice in BusinessProfileQuestionnaire.BRAND_PERSONALITY_CHOICES]
            if not isinstance(brand_personality, list):
                errors["brand_personality"] = "Must be a list of selected choices."
            else:
                invalid_choices = [choice for choice in brand_personality if choice not in valid_values]
                if invalid_choices:
                    errors["brand_personality"] = f"Invalid choices: {invalid_choices}. Choose from {valid_values}."

            content_atmosphere = business_data.get("content_atmosphere", [])
            valid_values = [choice[0] for choice in BusinessProfileQuestionnaire.CONTENT_ATMOSPERE_CHOICES]
            if not isinstance(content_atmosphere, list):
                errors["content_atmosphere"] = "Must be a list of selected choices."
            else:
                invalid_choices = [choice for choice in content_atmosphere if choice not in valid_values]
                if invalid_choices:
                    errors["content_atmosphere"] = f"Invalid choices: {invalid_choices}. Choose from {valid_values}."
                if len(content_atmosphere) > 3:
                    errors.setdefault("content_atmosphere", []).append("You can select up to 3 goals only.")

            business_keywords = business_data.get("business_keywords", [])
            if not isinstance(business_keywords, list):
                errors["business_keywords"] = ["Must be a list of words."]
            else:
                if not business_keywords:
                    if not isinstance(errors.get("business_keywords"), list):
                        errors["business_keywords"] = []
                    errors["business_keywords"].append("This field is required and cannot be empty.")
                elif not (5 <= len(business_keywords) <= 10):
                    if not isinstance(errors.get("business_keywords"), list):
                        errors["business_keywords"] = []
                    errors["business_keywords"].append("You must enter between 5 and 10 keywords.")
                if any(not isinstance(keyword, str) or not keyword.strip() for keyword in business_keywords):
                    if not isinstance(errors.get("business_keywords"), list):
                        errors["business_keywords"] = []
                    errors["business_keywords"].append("All keywords must be non-empty strings.")
            
            linguistic_style= business_data.get("linguistic_style", "").strip()
            valid_linguistic_style_choices = [choice[0] for choice in BusinessProfileQuestionnaire.LINGUISTIC_STYLE_CHOICES] 
            if not linguistic_style:
                errors["linguistic_style"] = "This field is required and cannot be empty."
            elif linguistic_style not in valid_linguistic_style_choices :
                errors["linguistic_style"] = f"Invalid choices: {invalid_choices}. Choose from {valid_linguistic_style_choices}."

            photo_style = business_data.get("photo_style", "").strip()
            valid_photo_choices = [choice[0] for choice in BusinessProfileQuestionnaire.PHOTO_STYLE_CHOICES]
            if not isinstance(photo_style, str):
                errors["photo_style"] = "Invalid input. Expected a string."
            elif photo_style not in valid_photo_choices:
                errors["photo_style"] = f"Invalid choice: '{photo_style}'. Choose from {valid_photo_choices}."
            if photo_style.lower() == "other":
                custom_photo = business_data.get("custom_photo_style", "").strip()
                if not custom_photo:
                    errors["custom_photo_style"] = "This field is required when 'other' is selected."

            favorite_colors= business_data.get("favorite_colors", "").strip()
            valid_favorite_colors_choices = [choice[0] for choice in BusinessProfileQuestionnaire.FAVORITE_COLORS_CHOICES]
            if not favorite_colors:
                errors["favorite_colors"] = "This field is required and cannot be empty."
            elif favorite_colors not in valid_favorite_colors_choices :
                errors["favorite_colors"] = f"Invalid choice. Choose from {valid_favorite_colors_choices}."

            photos_convey= business_data.get("photos_convey", "").strip()
            valid_photos_convey_choices = [choice[0] for choice in BusinessProfileQuestionnaire.PHOTOS_CONVEY_CHOICES] 
            if not photos_convey:
                errors["photos_convey"] = "This field is required and cannot be empty."
            elif not isinstance(photos_convey, str):
                errors["photos_convey"] = "Invalid input. Expected a string."
            elif photos_convey not in valid_photos_convey_choices:
                errors["photos_convey"] = f"Invalid choice: '{photos_convey}'. Choose from {valid_photos_convey_choices}."
            if photos_convey.lower() == "other":
                custom_photos_convey = business_data.get("custom_photos_convey", "").strip()
                if not custom_photos_convey:
                    errors["custom_photos_convey"] = "This field is required when 'other' is selected."
            
            post_sounds= business_data.get("post_sounds", "").strip()
            valid_post_sounds_choices = [choice[0] for choice in BusinessProfileQuestionnaire.POST_SOUNDS_CHOICES]
            if not post_sounds:
                errors["post_sounds"] = "This field is required and cannot be empty."
            elif post_sounds not in valid_post_sounds_choices :
                errors["post_sounds"] = f"Invalid choice. Choose from {valid_post_sounds_choices}."

            brand_colours = business_data.get("brand_colours", "").strip()
            valid_brand_colours_choices = [choice[0] for choice in BusinessProfileQuestionnaire.BRAND_COLOURS_CHOICES] 
            if not isinstance(brand_colours, str):
                errors["brand_colours"] = "Invalid input. Expected a string."
            elif brand_colours not in valid_brand_colours_choices: 
                errors["brand_colours"] = f"Invalid choice: '{brand_colours}'. Choose from {valid_brand_colours_choices}."

            logo = attrs.get("logo",None)
            if logo:
                allowed_extensions = ["png", "jpg", "jpeg", "svg"]
                if not any(logo.name.lower().endswith(ext) for ext in allowed_extensions):
                    errors["logo"] = "Invalid file type. Supported formats: PNG, JPG, JPEG, SVG."

        if page_num==7:
            avoided_content = business_data.get("avoided_content", "")
            if not isinstance(avoided_content, str):
                errors["avoided_content"] = "Invalid input format."
            sensitive_issue = business_data.get("sensitive_issue", "")
            if not isinstance(sensitive_issue, str):
                errors["sensitive_issue"] = "Invalid input format."
            key_messages = business_data.get("key_messages", "")
            if not isinstance(key_messages, str):
                errors["key_messages"] = "Invalid input format."
            brand_story_sentence = business_data.get("brand_story_sentence", "")
            if not isinstance(brand_story_sentence, str):
                errors["brand_story_sentence"] = "Invalid input format."

            success_metrics = business_data.get("success_metrics", [])
            valid_metrics = [choice[0] for choice in BusinessProfileQuestionnaire.SUCCESS_METRICS_CHOICES]
            if not isinstance(success_metrics, list):
                errors["success_metrics"] = "Must be a list of selected choices."
            else:
                invalid_choices = [choice for choice in success_metrics if choice not in valid_metrics]
                if invalid_choices:
                    errors["success_metrics"] = f"Invalid choices: {invalid_choices}. Choose from {valid_metrics}."
                if "other" in success_metrics:
                    custom_metric = business_data.get("custom_success_metric", "").strip()
                    if not custom_metric:
                        errors["custom_success_metric"] = "This field is required when 'Other' is selected."

            content_distribution = business_data.get("content_distribution")
            if content_distribution is None:
                errors["content_distribution"] = "This field is required and cannot be empty."
            elif not isinstance(content_distribution, list):
                errors["content_distribution"] = "Must be a list of category percentages."
            elif len(content_distribution) != 3:
                errors["content_distribution"] = "Must contain exactly three percentage values for educational, marketing, and narrative content."
            else:
                total_percentage = sum(content_distribution)
                if total_percentage != 100:
                    errors["content_distribution"] = "Total percentage must be exactly 100%."

            tone_examples = business_data.get("tone_examples", [])
            if not isinstance(tone_examples, list):
                errors["tone_examples"] = "Must be a list of example sentences."
            else:
                if not (3 <= len(tone_examples) <= 5):
                    errors["tone_examples"] = "You must provide between 3 to 5 examples."
                for index, example in enumerate(tone_examples, start=1):
                    if not isinstance(example, str) or not example.strip():
                        errors[f"tone_example_{index}"] = f"Example {index} cannot be empty and must be a string."

            formality_level = business_data.get("formality_level", "").strip()
            valid_formality_level_choices = [choice[0] for choice in BusinessProfileQuestionnaire.FORMALITY_CHOICES] 
            if not isinstance(formality_level, str):
                errors["formality_level"] = "Invalid input. Expected a string."
            elif formality_level not in valid_formality_level_choices: 
                errors["formality_level"] = f"Invalid choice: '{formality_level}'. Choose from {valid_formality_level_choices}."

            
        if errors:
            raise serializers.ValidationError(errors)
        return attrs

    def create(self, validated_data):
        business_data = validated_data.pop("business_data", {}) 
        instance = BusinessProfileQuestionnaire.objects.create(**validated_data, business_data=business_data)
        return instance

    def update(self, instance, validated_data):
        business_data = validated_data.pop("business_data", {}) 
        instance.business_data.update(business_data)
        instance.save()
        return instance
