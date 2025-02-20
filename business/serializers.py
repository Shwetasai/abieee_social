from business.models import BusinessDetails
from rest_framework import serializers
from .models import (
    BusinessDetails, BusinessProfileQuestionnaire, CommunicationPreferences,
    CommunicationStyle, ContentTypes, VisualStyle, SuccessMetrics
)

class BusinessDetailsSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')
    class Meta:
        model = BusinessDetails
        fields = ['id', 'business_name', 'field_of_activity', 'business_description', 'target_audience', 
                  'social_media_presence', 'social_media_link', 'goals_and_challenges', 'current_management','user']

class BusinessProfileQuestionnaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessProfileQuestionnaire
        fields = '__all__'


class CommunicationPreferencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunicationPreferences
        fields = '__all__'


class CommunicationStyleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunicationStyle
        fields = '__all__'


class ContentTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentTypes
        fields = '__all__'


class VisualStyleSerializer(serializers.ModelSerializer):
    class Meta:
        model = VisualStyle
        fields = '__all__'


class SuccessMetricsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuccessMetrics
        fields = '__all__'
