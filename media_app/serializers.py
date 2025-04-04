from rest_framework import serializers
from .models import MediaFile
from django.conf import settings

class MediaFileSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = MediaFile
        fields = '__all__'
        extra_kwargs = {'user': {'read_only': True}}

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')

        if instance.file and instance.file.name:
            file_url = instance.file.url 
            if request:
                representation['file'] = request.build_absolute_uri(file_url) 
            else:
                representation['file'] = settings.MEDIA_URL + instance.file.name 

        return representation

'''class SocialConnectSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialConnect
        fields = '__all__'
        read_only_fields = ['user']'''

'''class ScheduledPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduledPost
        fields = '__all__'
        read_only_fields = ['user', 'posted']'''