from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.utils.timezone import datetime
from rest_framework import status
from .models import MediaFile
from .serializers import MediaFileSerializer
from rest_framework.permissions import IsAuthenticated
class UploadMediaView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        serializer = MediaFileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetMediaByMonthView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, year, month, *args, **kwargs):
        media_files = MediaFile.objects.filter(uploaded_at__year=year, uploaded_at__month=month)
        serializer = MediaFileSerializer(media_files, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
