from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .serializers import CardInformationSerializer
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY 

class PaymentView(APIView):
    permission_classes = [AllowAny]
    serializer_class = CardInformationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            data_dict = serializer.validated_data

            try:
                payment_method = stripe.PaymentMethod.create(
                    type="card",
                    card={
                        #"number": data_dict['card_number'],
                        "exp_month": data_dict['expiry_month'],
                        "exp_year": data_dict['expiry_year'],
                        "cvc": data_dict['cvc'],
                    },
                )

                payment_intent = stripe.PaymentIntent.create(
                    amount=data_dict['amount'],
                    currency=data_dict['currency'],
                    payment_method=payment_method,
                    confirm=True,
                )

                return Response({
                    'message': "Payment successful",
                    'status': status.HTTP_200_OK,
                    'payment_intent': payment_intent.id
                }, status=status.HTTP_200_OK)

            except stripe.error.StripeError as e:
                return Response({
                    'message': "Payment failed",
                    'error': str(e),
                    'status': status.HTTP_400_BAD_REQUEST
                }, status=status.HTTP_400_BAD_REQUEST)

        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


