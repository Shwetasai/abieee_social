from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.utils.timezone import datetime
from rest_framework import status
from .models import MediaFile
from .serializers import MediaFileSerializer
from rest_framework.permissions import IsAuthenticated
from .models import MediaFile
from .serializers import MediaFileSerializer

class UploadMediaView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file_obj = request.FILES.get('file') 
        if not file_obj:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = MediaFileSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            media_file = serializer.save(user=request.user, file=file_obj)
            return Response(MediaFileSerializer(media_file, context={'request': request}).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        year = request.query_params.get('year')
        month = request.query_params.get('month')
        if not year or not month:
            return Response({"error": "Year and month are required parameters."}, status=400)
        try:
            year = int(year)
            month = int(month)
        except ValueError:
            return Response({"error": "Year and month must be integers."}, status=400)
        media_files = MediaFile.objects.filter(user=request.user, uploaded_at__year=year, uploaded_at__month=month)
        serializer = MediaFileSerializer(media_files, many=True, context={'request': request})
        return Response(serializer.data)
