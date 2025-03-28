from rest_framework import serializers
from preferences.models import SchedulingPreferences, PostDistribution

class SchedulingPreferencesSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = SchedulingPreferences
        fields = '__all__' 

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user  
        return super().create(validated_data)

class PostDistributionSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = PostDistribution
        fields = '__all__'

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user 
        return super().create(validated_data)
