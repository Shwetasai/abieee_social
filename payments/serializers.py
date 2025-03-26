import datetime
import stripe
from rest_framework import serializers

def check_payment_method(value):
    if value.lower() not in ["card"]:
        raise serializers.ValidationError("Invalid payment method.")

class CardInformationSerializer(serializers.Serializer):
    card_number = serializers.CharField(max_length=16, required=False)
    amount = serializers.IntegerField(required=True) 
    currency = serializers.CharField(max_length=3, required=False, allow_blank=True, default="usd")

    def create_payment_intent(self, validated_data):
        try:
            payment_intent = stripe.PaymentIntent.create(
                amount=validated_data["amount"],
                currency=validated_data["currency"],
                payment_method_types=["card"],
            )
            return {"client_secret": payment_intent.client_secret}
        except stripe.error.StripeError as e:
            raise serializers.ValidationError({"stripe_error": str(e)})