import datetime
import stripe
from rest_framework import serializers


def check_expiry_month(value):
    if not (1 <= value <= 12):
        raise serializers.ValidationError("Invalid expiry month.")

def check_expiry_year(value):
    current_year = datetime.datetime.now().year
    if value < current_year:
        raise serializers.ValidationError("Invalid expiry year.")

def check_cvc(value):
    if not value.isdigit() or not (3 <= len(value) <= 4):
        raise serializers.ValidationError("Invalid CVC number.")

def check_payment_method(value):
    if value.lower() not in ["card"]:
        raise serializers.ValidationError("Invalid payment method.")

class CardInformationSerializer(serializers.Serializer):
    card_number = serializers.CharField(max_length=16, required=False)
    expiry_month = serializers.IntegerField(validators=[check_expiry_month])
    expiry_year = serializers.IntegerField(validators=[check_expiry_year])
    cvc = serializers.CharField(max_length=4, required=True, validators=[check_cvc])
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