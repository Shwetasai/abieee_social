from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str
from django.core.mail import send_mail
from django.conf import settings
import re
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'password','confirm_password']
        
    def validate_password(self, attrs):
        password = self.initial_data.get('password')
        confirm_password = self.initial_data.get('confirm_password')
        errors={}
        if password != confirm_password:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})

        if len(password) < 8:
            raise serializers.ValidationError({"password": "Password must be at least 8 characters long."})
        if not re.search(r'\d', password):
            raise serializers.ValidationError({"password": "Password must contain at least one digit."})
        if not re.search(r'[A-Z]', password):
            raise serializers.ValidationError({"password": "Password must contain at least one uppercase letter."})
        if not re.search(r'[a-z]', password):
            raise serializers.ValidationError({"password": "Password must contain at least one lowercase letter."})
        if not re.search(r'[\W_]', password):
            raise serializers.ValidationError({"password": "Password must contain at least one special character (@$!%*#?&)."})

    
        return attrs
    def create(self, validated_data):
        password = validated_data.pop('password')
        
        confirm_password=validated_data.pop('confirm_password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user
    def forget_password(self,email):
        
        user = User.objects.filter(email=email).first()
        if not user:
            return {"message": "User with this email does not exist."}

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        reset_link = f"{settings.RESET_PASSWORD_URL}{uid}/{token}/"

        send_mail(
            "Password Reset Request",
            f"Click the link below to reset your password:\n{reset_link}",
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )
        return {"message": "Password reset link has been sent to your email."}
    