from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .serializers import CardInformationSerializer
import stripe
from django.conf import settings
from prices.models import Package
from .models import CardInformation, Payment
from rest_framework.permissions import IsAuthenticated

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
                amount=100 * 100,
                currency="usd",
                payment_method_types=["card"],
                payment_method="pm_card_visa",
                confirm=True,
                )

                card_info_data = {
                    "amount": data_dict.get("amount"),
                    "currency": data_dict.get("currency", "usd"),
                    }

                card_info = CardInformation.objects.create(**card_info_data)

                payment = Payment.objects.create(
                card_info=card_info,
                payment_intent_id=payment_intent.id,
                amount=card_info.amount,
                currency=card_info.currency,
                package=package,
                status="completed",
                )

                return Response({
                    'message': "Payment successful",
                    'status': status.HTTP_200_OK,
                    'payment_intent': payment_intent.id,
                    "payment_id": payment.payment_id,
                }, status=status.HTTP_200_OK)
            except stripe.error.StripeError as e:

                return Response({
                'message': "Payment failed",
                'error': "Payment intent was not created",
                'status': status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


