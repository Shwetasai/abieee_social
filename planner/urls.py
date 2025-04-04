from django.urls import path
from .views import PendingPostView, PostManagementView

urlpatterns = [
    path('pending-posts/', PendingPostView.as_view(), name='pending-posts'),
    path('manage-post/<str:post_id>/', PostManagementView.as_view(), name='post-management'),
    path('scheduled-posts/', PostManagementView.as_view(), name='scheduled-posts'),
    path('scheduled-posts/<str:status>/', PostManagementView.as_view(), name='filtered-posts'),
]
