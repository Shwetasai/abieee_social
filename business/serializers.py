from rest_framework import serializers
from business.models import (
    BusinessDetails, BusinessProfileQuestionnaire
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

