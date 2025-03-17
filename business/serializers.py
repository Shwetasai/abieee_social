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

    class Meta:
        model = BusinessProfileQuestionnaire
        fields = '__all__'

    PAGE_FIELDS = {
        1: ["business_size", "years_of_activity", "geographic_area_operation"],
        2: ["content_preference_type", "main_issues", "main_goals"],
        3: ["platform_preference","global_posting_frequency"],
        4: ["personal_business_story", "business_top_values", "special_strength","personal_twist","behind_brand_story"
            ,"complete_sentence","motivates","tell_friends","most_enjoyable","vision","believe"],
        5: [ "communication_style", "communication_preferences","describe_business","preferred_style","content_goals"],
        6: ["core_value","market_uniqueness","brand_personality","business_vision","content_atmosphere"
            ,"post_sounds","business_keywords","linguistic_style","photos_style","favorite_colour","photo_convey"],

        7: ["brand_story_sentence","success_metrics","content_distribution","tone_voice"],
    }
    ADDITIONAL_TEXT_FIELDS = ["business_top_values","personal_twist","personal_business_story","behind_brand_story"
    ]

    def validate(self, attrs):
        page_num = attrs.get("page_num")
        business_data = attrs.get("business_data", {})

        if not isinstance(business_data, dict):
            business_data = {}
        errors = {}

        if page_num in self.PAGE_FIELDS:
            missing_fields = [field for field in self.PAGE_FIELDS[page_num] if field not in business_data or not business_data[field]]
            if missing_fields:
                for field in missing_fields:
                    errors.setdefault(field, []).append("This field is required and cannot be empty.")
        if page_num == 2 or attrs.get("is_success", False):
            content_preference = business_data.get("content_preference_type", [])
            if not isinstance(content_preference, list):
                content_preference = [content_preference] if content_preference else []
            if "Other" in content_preference and not business_data.get("other_preferred_content_types"):
                errors["other_preferred_content_types"] = ["This field is required when 'Other' is selected."]

        if page_num == 3 or attrs.get("is_success", False):
            platform_preference = business_data.get("platform_preference", {})
            platform_selection = business_data.get("platform_selection", "")

            if not platform_selection and not any(platform in platform_preference for platform in ["Linkedin", "Facebook", "Instagram", "Tiktok"]):
                errors.setdefault("platform_selection", []).append("Please select at least one platform.")

        if page_num == 4 or attrs.get("is_success", False):
            for field in self.ADDITIONAL_TEXT_FIELDS:
                selected_values = business_data.get(field, [])
                additional_text_data = business_data.get(f"{field}_text", {})

                if not isinstance(selected_values, list):
                    selected_values = [selected_values] if selected_values else []

                if not isinstance(additional_text_data, dict):
                    additional_text_data = {}

                for value in selected_values:
                    if value and value not in additional_text_data:
                        errors.setdefault(f"{field}_text[{value}]", []).append(
                            f"Please provide additional text for the selected '{value}' in '{field}'."
                        )
            
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
