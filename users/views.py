from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from users.serializers import UserRegistrationSerializer
from users.models import User
from rest_framework.permissions import AllowAny  
import base64
from django.core.mail import send_mail
from django.conf import settings
import jwt
from datetime import datetime, timedelta
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str
from rest_framework import serializers
from jwt.exceptions import ExpiredSignatureError
from rest_framework.authentication import SessionAuthentication
class UserRegistrationView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    
    def post(self, request):
        
        email = request.data.get('email')
        
        existing_user = User.objects.filter(email=email).first()
        

        if existing_user:
            if existing_user.is_email_verified:
                return Response(
                    {"message": "This email is already verified. Please log in."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            else:
                self.send_verification_email(request, existing_user, "send Verification Email - AIBee-social")
                return Response(
                    {"message": "Verification email Resent successfully. Please check your inbox."},
                    status=status.HTTP_200_OK
                )
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            self.send_verification_email(request, user, "Welcome to AIBee-social!")
            return Response(
                {"message": "Verification email sent successfully. Please check your inbox to complete registration."},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def get(self, request, *args, **kwargs):
        token = request.query_params.get('token')
        if not token:
            return Response(
                {"message": "Invalid verification link. Please try again."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])

            if payload['exp'] < datetime.utcnow().timestamp():
                return Response(
                    {"message": "Verification link has expired. Please request a new one."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            encoded_email = payload.get('email')
            decoded_email = base64.urlsafe_b64decode(encoded_email).decode()

            user = User.objects.filter(email=decoded_email).first()

            if not user:
                return Response(
                    {"message": "User not found. Please register again."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if user.is_email_verified:
                return Response(
                    {"message": "This email is already verified. Please log in."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            user.is_email_verified = True
            user.save()

            return Response(
                {"message": "Your email has been verified successfully. Registration is now complete."},
                status=status.HTTP_200_OK
            )
        
        except ExpiredSignatureError:
            return Response(
                {"message": "Verification link has expired. Please request a new one."},
                status=status.HTTP_400_BAD_REQUEST
            )

    def send_verification_email(self, request, user, subject):
        encoded_email = base64.urlsafe_b64encode(user.email.encode()).decode()

        payload = {
            "email": encoded_email,
            "exp": datetime.utcnow() + timedelta(minutes=1),
        }

        verification_token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

        verification_link = f"{request.scheme}://{request.get_host()}/api/users/verify/?token={verification_token}"

        send_mail(
            subject=subject,
            message=f"Click the link to verify your email: {verification_link}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )
class LoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({"message": "Email and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        
        user = User.objects.filter(email=email).first()
        if user is None:
            return Response({"message": "User with this email not found. Please register first."}, status=status.HTTP_400_BAD_REQUEST)

        if not user.is_email_verified:
            return Response({"message": "Email is not verified.please check your Email"})
        if user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({
                    'message': 'Login successful.',
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status=status.HTTP_200_OK)
        return Response({"message": "Incorrect email or password.Please check your email or password and try again."}, status=status.HTTP_400_BAD_REQUEST)
        

class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response({"message": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = UserRegistrationSerializer()
        response = serializer.forget_password(email)
        if 'message' in response:
            return Response({"message": response["message"]}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "An error occurred."}, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    def post(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({"message": "Invalid reset link."}, status=status.HTTP_400_BAD_REQUEST)

        if not default_token_generator.check_token(user, token):
            return Response({"message": "Reset link is invalid or expired."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserRegistrationSerializer(data=request.data, partial=True)

        if serializer.is_valid():
            user.set_password(serializer.validated_data["password"])
            user.save()
            return Response({"message": "Password has been updated successfully."}, status=status.HTTP_200_OK)
        else:
            print("Serializer Errors:", serializer.errors)
            return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST) 
class SuccessfullLogin(APIView):
    permission_classes = [AllowAny]
    def get(self, request, format=None):
        user = request.user
        
        if user.is_authenticated:
            if not user.username:
                user.username = user.email
                user.save()
            return Response({
                    "message": "Login successful",
                    "username": user.username,
                    "email": user.email,
                }, status=status.HTTP_200_OK)
            
        return Response({"error": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

from django.http import HttpResponse

def home(request):
    return HttpResponse("Hello, Django!")


