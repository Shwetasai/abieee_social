from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from planner.models import PendingPost, Post
from .serializers import PendingPostSerializer, PostSerializer
from django.utils import timezone
from datetime import datetime

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