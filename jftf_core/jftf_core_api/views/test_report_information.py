from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from ..models import TestReportInformation
from ..serializers import TestReportInformationSerializer


class TestReportInformationModelViewSet(viewsets.ModelViewSet):
    """
    ModelViewSet for CRUD operations on TestReportInformation objects.
    """
    queryset = TestReportInformation.objects.all()
    serializer_class = TestReportInformationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['testId', 'executionResult']
    pagination_class = None
