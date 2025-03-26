from django.urls import path
from .views import SchedulingPreferencesView, PostDistributionView

urlpatterns = [
    path('scheduling-preferences/', SchedulingPreferencesView.as_view(), name='scheduling-preferences'),
    path('post-distribution/', PostDistributionView.as_view(), name='post-distribution'),
]
