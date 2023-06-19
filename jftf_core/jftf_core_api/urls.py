from django.urls import path, include
from django.conf import settings
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from .views import TestCaseMetadataModelViewSet, TestCaseModelViewSet, TestCaseAdminModelViewSet, \
    TestReportInformationModelViewSet, TestReportModelViewSet, TaskResultViewSet, TaskResultAdminViewSet

api_router = DefaultRouter()
api_router.register(r'test-case-metadata', TestCaseMetadataModelViewSet, basename='test-case-metadata')
api_router.register(r'test-case', TestCaseModelViewSet, basename='test-case')
api_router.register(r'test-case-admin', TestCaseAdminModelViewSet, basename='test-case-admin')
api_router.register(r'test-report-information', TestReportInformationModelViewSet, basename='test-report-information')
api_router.register(r'test-report', TestReportModelViewSet, basename='test-report')
api_router.register(r'test-case-result', TaskResultViewSet, basename='test-case-result')
api_router.register(r'test-case-result-admin', TaskResultAdminViewSet, basename='test-case-result-admin')

urlpatterns = [
    path('token-auth/', views.obtain_auth_token),
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
