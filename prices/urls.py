from django.urls import path
from .views import PackageListCreateView

urlpatterns = [
    path('packages/', PackageListCreateView.as_view(), name='package-list'),
    path('packages/<int:pk>/', PackageListCreateView.as_view(), name='package-list'),
]
