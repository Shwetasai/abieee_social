
from .serializers import (BusinessDetailsSerializer,BusinessProfileQuestionnaireSerializer)
from business.models import (BusinessDetails,
BusinessProfileQuestionnaire
)
from django.db import models
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import ValidationError
class BusinessDetailsListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk=None):
        if pk:
            business = get_object_or_404(BusinessDetails, pk=pk)
            serializer = BusinessDetailsSerializer(business)
        else:
            businesses = BusinessDetails.objects.all()
            serializer = BusinessDetailsSerializer(businesses, many=True)
        return Response(serializer.data)

    def post(self, request):
        if BusinessDetails.objects.filter(user=request.user).exists():
            return Response({"error": "You already have a business profile"}, status=status.HTTP_400_BAD_REQUEST)


        serializer = BusinessDetailsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request,pk=None):
        instance = get_object_or_404(BusinessDetails, pk=pk)
        serializer = BusinessDetailsSerializer(instance, data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BusinessProfileQuestionnaireView(APIView):
    def get(self, request, pk=None):
        if pk:
            questionnaire = get_object_or_404(BusinessProfileQuestionnaire, pk=pk)
            serializer = BusinessProfileQuestionnaireSerializer(questionnaire)
            return Response(serializer.data)
        else:
            questionnaires = BusinessProfileQuestionnaire.objects.all()
            serializer = BusinessProfileQuestionnaireSerializer(questionnaires, many=True)
            return Response(serializer.data)

    def post(self, request):
        page_data = request.data
        page_num = page_data.get('page', 1)
        business_id = page_data.get('business', None)

        if not business_id:
            return Response({"error": "Business ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            business = BusinessDetails.objects.get(id=business_id)
        except BusinessDetails.DoesNotExist:
            return Response({"error": "Business ID not found."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            questionnaire, created = BusinessProfileQuestionnaire.objects.get_or_create(business=business)
            serializer = BusinessProfileQuestionnaireSerializer(questionnaire, data=page_data, partial=True)

            if page_num in range(1, 8):
                required_fields = []
                if page_num == 1:
                    required_fields = ['core_business_values', 'unique_selling_proposition', 'business_voice', 'business_voice_other']
                elif page_num == 2:
                    required_fields = ['main_customers', 'customers_language', 'main_challenges', 'business_challenges_solution', 'communication_tone', 'emoji_usage']
                elif page_num == 3:
                    required_fields = ['important_phrases', 'phrases_avoid', 'writing_style', 'additional_communication_preferences']
                elif page_num == 4:
                    required_fields = ['content_type_preference', 'educational_content_percentage', 'promotional_content_percentage', 'behind_the_scenes_percentage', 'inspirational_content_percentage', 'seasonal_content_description']
                elif page_num == 5:
                    required_fields = ['primary_color', 'secondary_color', 'accent_color', 'preferred_visual_style', 'image_type_preferences', 'additional_design_notes']
                elif page_num == 6:
                    required_fields = ['successful_post_examples', 'inspiring_brands', 'most_successful_post', 'made_successful']
                elif page_num == 7:
                    required_fields = ['successful_post_definition', 'business_goals', 'topics_to_avoid', 'additional_guidelines']

                for field in required_fields:
                    if field not in page_data:
                        return Response({"error": f"Missing required field: {field} for page {page_num}"}, status=status.HTTP_400_BAD_REQUEST)

            if serializer.is_valid():
                serializer.save()
                return Response({"message": f"Page {page_num} data saved.", "data": serializer.data}, status=status.HTTP_200_OK if not created else status.HTTP_201_CREATED)
            else:
                return Response({"errors": serializer.errors, "message": f"Page {page_num} data validation failed."}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, pk):
        questionnaire = get_object_or_404(BusinessProfileQuestionnaire, pk=pk)
        serializer = BusinessProfileQuestionnaireSerializer(questionnaire, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)