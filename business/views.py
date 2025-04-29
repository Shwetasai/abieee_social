'''
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
    def post(self, request):

        user = request.user 
        business_profile = BusinessProfileQuestionnaire.objects.filter(user=user).first()

        if business_profile:
            serializer = BusinessProfileQuestionnaireSerializer(business_profile, data=request.data, partial=True)
        else:
            serializer = BusinessProfileQuestionnaireSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=user) 
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def put(self, request, pk):
        questionnaire = get_object_or_404(BusinessProfileQuestionnaire, pk=pk)
        serializer = BusinessProfileQuestionnaireSerializer(questionnaire, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            page_num = request.data.get("page_num")
            message = f"Page {page_num} data updated." if page_num else "Data has been updated."

            return Response({"message": message, "data": serializer.data}, status=status.HTTP_200_OK)
    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk=None):
        if pk:
            questionnaire = get_object_or_404(BusinessProfileQuestionnaire, pk=pk)
            serializer = BusinessProfileQuestionnaireSerializer(questionnaire)
            return Response(serializer.data)
        else:
            questionnaires = BusinessProfileQuestionnaire.objects.all()
            serializer = BusinessProfileQuestionnaireSerializer(questionnaires, many=True)
            return Response(serializer.data)

'''

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import BusinessDetails, BusinessProfileQuestionnaire
from .serializers import BusinessDetailsSerializer, BusinessProfileQuestionnaireSerializer

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
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
