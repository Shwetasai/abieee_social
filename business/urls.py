from business.views import (BusinessDetailsView,BusinessProfileQuestionnaireView)
from django.urls import path
urlpatterns =[
path('business_details/', BusinessDetailsView.as_view(), name='business_list'),
path('business_details/<int:pk>/', BusinessDetailsView.as_view(), name='business_list'),
path('business-profile-questionnaire/', BusinessProfileQuestionnaireView.as_view(), name='business-profile-questionnaire'),
path('business-profile-questionnaire/<int:pk>/', BusinessProfileQuestionnaireView.as_view(), name='business_profile_questionnaire_detail'),


]

