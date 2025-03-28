from rest_framework import serializers
from .models import PendingPost, Post

class PendingPostSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    post_id = serializers.UUIDField(read_only=True)

    class Meta:
        model = PendingPost
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['content', 'media', 'post_type', 'platform', 'scheduling_date', 'content_status', 'user', 'post_id', 'media_status']

