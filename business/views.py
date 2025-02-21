
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
class BusinessDetailsListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request,pk=None):
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
    def get(self, request,pk=None):
        if pk:
            questionnaire = get_object_or_404(BusinessProfileQuestionnaire, pk=pk)
            serializer = BusinessProfileQuestionnaireSerializer(questionnaire)
        else:
            questionnaires = BusinessProfileQuestionnaire.objects.all()
            serializer = BusinessProfileQuestionnaireSerializer(questionnaires, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BusinessProfileQuestionnaireSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request,pk=None):
        instance = get_object_or_404(BusinessProfileQuestionnaire,pk=pk)
        serializer = BusinessProfileQuestionnaireSerializer(instance, data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

