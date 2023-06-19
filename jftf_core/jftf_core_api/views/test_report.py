from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from .pagination import ContentRangeHeaderPagination
from ..models import TestReports
from ..serializers import TestReportSerializer


class TestReportModelViewSet(viewsets.ModelViewSet):
    """
    ModelViewSet for CRUD operations on TestReports objects.
    """
    queryset = TestReports.objects.all()
    serializer_class = TestReportSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['reportId', 'testId', 'testReportInformationId']
    pagination_class = None
