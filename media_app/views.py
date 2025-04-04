from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.utils.timezone import datetime
from rest_framework import status
from .serializers import MediaFileSerializer
from rest_framework.permissions import IsAuthenticated
from .models import MediaFile
import requests
from django.conf import settings

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
            post_response = self.post_to_instagram(request.user, media_file)
            if "id" in post_response:
                media_file.instagram_post_id = post_response["id"]
                media_file.save()
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
    
    '''def post_to_instagram(self, user, media_file):

        try:
            
            access_token = settings.INSTAGRAM_ACCESS_TOKEN
            instagram_account_id = settings.INSTAGRAM_ACCOUNT_ID

            if not access_token or not instagram_account_id:
                return {"error": "Instagram account not linked"}

            image_url = media_file.file.url
            caption = "Posted via Django!"

            upload_url = f"https://graph.facebook.com/v19.0/{instagram_account_id}/media"
            payload = {
                "image_url": image_url,
                "caption": caption,
                "access_token": access_token
            }

            upload_response = requests.post(upload_url, data=payload)
            upload_result = upload_response.json()

            if "id" in upload_result:
                creation_id = upload_result["id"]

                publish_url = f"https://graph.facebook.com/v19.0/{instagram_account_id}/media_publish"
                publish_payload = {
                    "creation_id": creation_id,
                    "access_token": access_token
                }
                publish_response = requests.post(publish_url, data=publish_payload)

                return publish_response.json()

            return upload_result

        except Exception as e:
            return {"error": str(e)}

'''