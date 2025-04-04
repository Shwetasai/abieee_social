from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from planner.models import PendingPost, Post
from .serializers import PendingPostSerializer, PostSerializer
from prices.models import Package
from payments.models import UserPackage
from instagrapi import Client
import os
from django.conf import settings
import datetime
INSTAGRAM_USERNAME = settings.INSTAGRAM_USERNAME
INSTAGRAM_PASSWORD = settings.INSTAGRAM_PASSWORD

class PendingPostView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        posts = PendingPost.objects.filter(user=request.user)
        serializer = PendingPostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PendingPostSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            post = serializer.save(user=request.user)
            user_package = UserPackage.objects.filter(user=request.user).first()
            if user_package and (user_package.posts_per_month == 0 or user_package.credits == 0):
                recommended_package = Package.objects.filter(price__gt=user_package.package.price).order_by('price').first()
                if recommended_package:
                    return Response({
                        "message": "Post created successfully, but you are out of credits or posts. Upgrade recommended!",
                        "post_id": post.post_id,
                        "recommended_package": recommended_package.package_type
                    }, status=status.HTTP_201_CREATED)
            return Response({"message": "Pending post added successfully!", "post_id": post.post_id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostManagementView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id, *args, **kwargs):
        action = request.data.get('action')
        if action not in ['approve', 'cancel']:
            return Response({'error': 'Invalid or missing action (must be "approve" or "cancel")'}, status=400)

        pending_post = get_object_or_404(PendingPost, post_id=post_id, user=request.user)
        
        try:
            pending_post.content_status = 'approved' if action == 'approve' else 'canceled'
            pending_post.media_status = 'approved' if action == 'approve' else 'canceled'
            pending_post.save(update_fields=['content_status', 'media_status'])
            if action == 'approve':
                post = Post.objects.create(
                    user=request.user,
                    post_id=pending_post.post_id,
                    content="Approved post", 
                    media=getattr(pending_post, 'media', None), 
                    post_type=pending_post.post_type,
                    platform=pending_post.platform,
                    scheduling_date=datetime.datetime.combine(
                        pending_post.publication_date,
                        pending_post.publication_time
                    )
                )

                if pending_post.platform == 'instagram':
                    try:
                        cl = Client()
                        cl.login(settings.INSTAGRAM_USERNAME, settings.INSTAGRAM_PASSWORD)

                        image_path = os.path.join(settings.MEDIA_ROOT, str(post.media))
                        caption = post.content or "Shared via our platform!"

                        if os.path.exists(image_path):
                            media = cl.photo_upload(image_path, caption)
                            print("Uploaded to Instagram:", media.dict())
                        else:
                            return Response({"error": "Media file not found for Instagram post"}, status=404)

                    except Exception as e:
                        return Response({"error": f"Instagram upload failed: {str(e)}"}, status=500)


            return Response({
                "message": f"Post {action}d successfully",
                "content_status": pending_post.content_status,
                "media_status": pending_post.media_status
            }, status=200)

        except Exception as e:
            return Response({'error': f"An error occurred: {str(e)}"}, status=500)
        

    def get(self, request, *args, **kwargs):
        status_filter = request.GET.get('status')
        if status_filter:
            posts = PendingPost.objects.filter(content_status=status_filter)
        else:
            posts = PendingPost.objects.all()

        serializer = PendingPostSerializer(posts, many=True)
        return Response(serializer.data)