from business.views import (BusinessDetailsListCreateView,BusinessProfileQuestionnaireView,CommunicationPreferencesView,CommunicationStyleView,
ContentTypesView,VisualStyleView,SuccessMetricsView)
from django.urls import path
urlpatterns =[
path('business_details/', BusinessDetailsListCreateView.as_view(), name='business_list'),
path('business-profile-questionnaire/', BusinessProfileQuestionnaireView.as_view(), name='business-profile-questionnaire'),
path('communication-preferences/', CommunicationPreferencesView.as_view(), name='communication-preferences'),
path('communication-style/', CommunicationStyleView.as_view(), name='communication-style'),
path('content-types/', ContentTypesView.as_view(), name='content-types'),
path('visual-style/', VisualStyleView.as_view(), name='visual-style'),
path('success-metrics/', SuccessMetricsView.as_view(), name='success-metrics'),
path('business_details/<int:pk>/', BusinessDetailsListCreateView.as_view(), name='business_details_detail'),
path('business-profile-questionnaire/<int:pk>/', BusinessProfileQuestionnaireView.as_view(), name='business_profile_questionnaire_detail'),
path('communication-preferences/<int:pk>/', CommunicationPreferencesView.as_view(), name='communication_preferences_detail'),
path('communication-style/<int:pk>/', CommunicationStyleView.as_view(), name='communication_style_detail'),
path('content-types/<int:pk>/', ContentTypesView.as_view(), name='content_types_detail'),
path('visual-style/<int:pk>/', VisualStyleView.as_view(), name='visual_style_detail'),
path('success-metrics/<int:pk>/', SuccessMetricsView.as_view(), name='success_metrics_detail'),


]