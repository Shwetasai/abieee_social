from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from .serializers import CardInformationSerializer
from .models import CardInformation, Payment
from prices.models import Package
import stripe
from datetime import date, timedelta
from .models import UserPackage
from django.utils import timezone
stripe.api_key = settings.STRIPE_SECRET_KEY 
class PaymentView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CardInformationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        package_id = request.data.get("package_id")

        if not package_id:
            return Response({"error": "Package ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            package = Package.objects.get(id=package_id)
        except Package.DoesNotExist:
            return Response({"error": "Invalid package ID"}, status=status.HTTP_404_NOT_FOUND)
        
        if serializer.is_valid():
            data_dict = serializer.validated_data
            try:
                payment_intent = stripe.PaymentIntent.create(
                    amount=package.price * 100, 
                    currency="usd",
                    payment_method_types=["card"],
                    payment_method="pm_card_visa",
                    confirm=True,
                )
                card_info = CardInformation.objects.create(
                    amount=data_dict.get("amount"),
                    currency=data_dict.get("currency", "usd"),
                )
                payment = Payment.objects.create(
                    card_info=card_info,
                    payment_intent_id=payment_intent.id,
                    amount=card_info.amount,
                    currency=card_info.currency,
                    package=package,
                    status="completed",
                )

                user_package = UserPackage.objects.filter(user=request.user).first()

                if user_package and user_package.end_date >= timezone.now().date():
                    user_package.end_date += timedelta(days=30)
                    user_package.posts_per_month += package.posts_per_month
                    user_package.credits += package.credits
                    user_package.save(update_fields=['end_date', 'posts_per_month', 'credits'])
                    user_package_status = "updated"
                else:
                    user_package = UserPackage.objects.create(
                        user=request.user,
                        package=package,
                        package_type=package.package_type,
                        price=package.price,
                        platforms=package.platforms,
                        posts_per_month=package.posts_per_month,
                        credits=package.credits,
                        content_text=package.content_text,
                        content_photos=package.content_photos,
                        content_video=package.content_video,
                        editing=package.editing,
                        history=package.history,
                        start_date=date.today(),
                        end_date=date.today() + timedelta(days=30),
                    )
                    user_package_status = "created"

                return Response({
                    "message": "Payment successful",
                    "status": status.HTTP_200_OK,
                    "payment_intent": payment_intent.id,
                    "payment_id": payment.payment_id,
                    "user_package_status": user_package_status,
                }, status=status.HTTP_200_OK)

            except stripe.error.StripeError as e:
                return Response({
                    "message": "Payment failed",
                    "error": str(e),
                    "status": status.HTTP_400_BAD_REQUEST
                }, status=status.HTTP_400_BAD_REQUEST)

        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)