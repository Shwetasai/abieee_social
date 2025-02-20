
from .serializers import (BusinessDetailsSerializer,BusinessProfileQuestionnaireSerializer,CommunicationPreferencesSerializer,
CommunicationStyleSerializer,ContentTypesSerializer,VisualStyleSerializer,SuccessMetricsSerializer)
from business.models import (BusinessDetails,CommunicationPreferences,CommunicationStyle,ContentTypes,VisualStyle,SuccessMetrics,
BusinessProfileQuestionnaire
)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
class BusinessDetailsListCreate(APIView):
    def get(self, request,pk=None):
        if pk:
            business = get_object_or_404(BusinessDetails, pk=pk)
            serializer = BusinessDetailsSerializer(business)
        else:
            businesses = BusinessDetails.objects.all()
            serializer = BusinessDetailsSerializer(businesses, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BusinessDetailsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request,pk):
        instance = get_object_or_404(BusinessDetails, pk=pk)
        serializer = BusinessDetailsSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BusinessProfileQuestionnaire(APIView):
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

    def put(self, request,pk):
        instance = get_object_or_404(BusinessProfileQuestionnaire,pk=pk)
        serializer = BusinessProfileQuestionnaireSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CommunicationPreferences(APIView):
    def get(self, request, pk=None):
        if pk:
            preference = get_object_or_404(CommunicationPreferences, pk=pk)
            serializer = CommunicationPreferencesSerializer(preference)
        else:
            preferences = CommunicationPreferences.objects.all()
            serializer = CommunicationPreferencesSerializer(preferences, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CommunicationPreferencesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request,pk):
        instance = get_object_or_404(CommunicationPreferences,pk=pk)
        serializer = CommunicationPreferencesSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CommunicationStyle(APIView):
    def get(self, request,pk=None):
        if pk:
            style = get_object_or_404(CommunicationStyle, pk=pk)
            serializer = CommunicationStyleSerializer(style)
        else:
            styles = CommunicationStyle.objects.all()

            serializer = CommunicationStyleSerializer(styles, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CommunicationStyleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def put(self, request,pk):
        instance = get_object_or_404(CommunicationStyle,pk=pk)
        serializer = CommunicationStyleSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ContentTypes(APIView):
    def get(self, request,pk=None):
        if pk:
            types = get_object_or_404(ContentTypes, pk=pk)
            serializer = ContentTypesSerializer(types)
        else:
            types = ContentTypes.objects.all()
            serializer = ContentTypesSerializer(types, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ContentTypesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request,pk):
        instance = get_object_or_404(ContentTypes,pk=pk)
        serializer = ContentTypesSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class VisualStyle(APIView):
    def get(self, request,pk=None):
        if pk:
            style = get_object_or_404(VisualStyle, pk=pk)
            serializer = VisualStyleSerializer(style)
        else:
            styles = VisualStyle.objects.all()
            serializer = VisualStyleSerializer(styles, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = VisualStyleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request,pk):
        instance = get_object_or_404(VisualStyle,pk=pk)

        serializer = VisualStyleSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class SuccessMetrics(APIView):
    def get(self, request,pk=None):
        if pk:
            metrics = get_object_or_404(SuccessMetrics, pk=pk)
            serializer = SuccessMetricsSerializer(metrics)
        else:
            metrics = SuccessMetrics.objects.all()
            serializer = SuccessMetricsSerializer(metrics, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SuccessMetricsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def put(self, request,pk):
        instance = get_object_or_404(SuccessMetrics,pk=pk)
        serializer = SuccessMetricsSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
