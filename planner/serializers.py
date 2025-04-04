from rest_framework import serializers
from .models import PendingPost, Post
from payments.models import UserPackage
from django.utils import timezone

class PendingPostSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    post_id = serializers.UUIDField(read_only=True)

    class Meta:
        model = PendingPost
        fields = '__all__'

    def validate(self, data):
        user = self.context['request'].user
        user_package = UserPackage.objects.filter(user=user).order_by('-end_date').first()

        if not user_package:
            raise serializers.ValidationError("User does not have an active package.")
        if user_package.end_date < timezone.now().date():
            raise serializers.ValidationError("Your package has expired. Please renew to continue posting.")
        if user_package.credits < 1:
            raise serializers.ValidationError("Not enough credits to post. Please upgrade your plan.")
        return data

    def create(self, validated_data):
        user = self.context['request'].user
        user_package = UserPackage.objects.filter(user=user).first()
        upload_type = validated_data.get('upload_type', 'self')
        if upload_type == 'system':
            total_deduction = 2 
        else:
            total_deduction = 1
        if user_package.credits < total_deduction:
            raise serializers.ValidationError("Not enough credits to post. Please upgrade your plan.")
        user_package.credits -= total_deduction
        user_package.posts_per_month -= 1
        user_package.save(update_fields=['credits', 'posts_per_month'])
        if user_package.credits < 1:
            raise serializers.ValidationError("Not enough credits to post. Please upgrade your plan.")

        return super().create(validated_data)

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['content', 'media', 'post_type', 'platform', 'scheduling_date', 'content_status', 'user', 'post_id', 'media_status']

