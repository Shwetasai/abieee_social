from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated 
from preferences.serializers import SchedulingPreferencesSerializer, PostDistributionSerializer

class SchedulingPreferencesView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = SchedulingPreferencesSerializer(data=request.data, context={'request': request})  
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Preferences saved successfully!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostDistributionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PostDistributionSerializer(data=request.data, context={'request': request}) 
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Post distribution saved successfully!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
