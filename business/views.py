
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import BusinessDetails, BusinessProfileQuestionnaire
from .serializers import BusinessDetailsSerializer, BusinessProfileQuestionnaireSerializer
from business.utils.monday_service import create_item
class BusinessDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        business = get_object_or_404(BusinessDetails, user=request.user)
        serializer = BusinessDetailsSerializer(business)
        return Response(serializer.data)

    def post(self, request):
        if BusinessDetails.objects.filter(user=request.user).exists():
            return Response({"error": "You already have a business profile"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = BusinessDetailsSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        business_instance = serializer.save(user=request.user)

        board_id = request.data.get("board_id")
        business_name = request.data.get("business_name")
        field_of_activity = request.data.get("field_of_activity")
        business_description = request.data.get("business_description")
        target_audience= request.data.get("target_audience")


        if not all([board_id, ]):
            return Response({"error": "Missing required fields for Monday.com"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            board_id = int(board_id)
            monday_response = create_item(board_id,business_name,field_of_activity, business_description,target_audience)

            return Response({
                "message": "Business profile created successfully",
                "business_data": serializer.data,
                "monday_response": monday_response
            }, status=status.HTTP_201_CREATED)

        except ValueError:
            return Response({"error": "Invalid board_id, must be an integer"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": "Failed to send data to Monday.com", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def put(self, request):
        business = get_object_or_404(BusinessDetails, user=request.user)
        serializer = BusinessDetailsSerializer(business, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BusinessProfileQuestionnaireView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        questionnaire, created = BusinessProfileQuestionnaire.objects.get_or_create(user=request.user, defaults={})

        if 'logo' in request.FILES:
            questionnaire.logo = request.FILES['logo']
        serializer = BusinessProfileQuestionnaireSerializer(questionnaire, data=request.data, partial=True)
        if serializer.is_valid():
            instance = serializer.save()
            if 'logo' in request.FILES:
                instance.logo = request.FILES['logo']
                instance.save()

            return Response({
            "message": "Data updated successfully.",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def put(self, request):
        questionnaire = get_object_or_404(BusinessProfileQuestionnaire, user=request.user)
        serializer = BusinessProfileQuestionnaireSerializer(questionnaire, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            page_num = request.data.get("page_num")
            message = f"Page {page_num} data updated." if page_num else "Data updated successfully."
            return Response({"message": message, "data": serializer.data}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        questionnaire = get_object_or_404(BusinessProfileQuestionnaire, user=request.user)
        serializer = BusinessProfileQuestionnaireSerializer(questionnaire)
        return Response(serializer.data, status=status.HTTP_200_OK)
