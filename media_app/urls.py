from django.urls import path
from .views import UploadMediaView, GetMediaByMonthView

urlpatterns = [
    path('upload/', UploadMediaView.as_view(), name='upload-media'),
    path('media/<int:year>/<int:month>/', GetMediaByMonthView.as_view(), name='media-by-month'),
]
