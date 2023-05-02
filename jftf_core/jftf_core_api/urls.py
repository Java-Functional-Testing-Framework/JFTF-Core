from django.urls import path, include
from django.conf import settings
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter
from .views import TestCaseMetadataModelViewSet

api_router = DefaultRouter()
api_router.register(r'test-case-metadata', TestCaseMetadataModelViewSet, basename='test-case-metadata')

urlpatterns = [
    path('auth/', include('allauth.urls')),
    path('rest-auth/', include('dj_rest_auth.urls')),
    path('', include(api_router.urls)),
]

swagger_spectacular_url_patterns = [
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]


if settings.DEBUG:
    [urlpatterns.append(url_pattern) for url_pattern in swagger_spectacular_url_patterns]
