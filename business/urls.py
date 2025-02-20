from business.views import (BusinessDetailsListCreate,BusinessProfileQuestionnaire,CommunicationPreferences,CommunicationStyle,
ContentTypes,VisualStyle,SuccessMetrics)
from django.urls import path
urlpatterns =[
path('business_details/', BusinessDetailsListCreate.as_view(), name='business_list'),
path('business-profile-questionnaire/', BusinessProfileQuestionnaire.as_view(), name='business-profile-questionnaire'),
path('communication-preferences/', CommunicationPreferences.as_view(), name='communication-preferences'),
path('communication-style/', CommunicationStyle.as_view(), name='communication-style'),
path('content-types/', ContentTypes.as_view(), name='content-types'),
path('visual-style/', VisualStyle.as_view(), name='visual-style'),
path('success-metrics/', SuccessMetrics.as_view(), name='success-metrics'),
path('business_details/<int:pk>/', BusinessDetailsListCreate.as_view(), name='business_details_detail'),
path('business_profile_questionnaire/<int:pk>/', BusinessProfileQuestionnaire.as_view(), name='business_profile_questionnaire_detail'),
path('communication_preferences/<int:pk>/', CommunicationPreferences.as_view(), name='communication_preferences_detail'),
path('communication_style/<int:pk>/', CommunicationStyle.as_view(), name='communication_style_detail'),
path('content_types/<int:pk>/', ContentTypes.as_view(), name='content_types_detail'),
path('visual_style/<int:pk>/', VisualStyle.as_view(), name='visual_style_detail'),
path('success_metrics/<int:pk>/', SuccessMetrics.as_view(), name='success_metrics_detail'),


]