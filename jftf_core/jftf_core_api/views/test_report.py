from rest_framework import viewsets, permissions
from django_filters.filters import OrderingFilter, CharFilter
from django_filters import FilterSet
from django_filters.rest_framework import DjangoFilterBackend
from .pagination import ContentRangeHeaderPagination
from ..models import TestReports
from ..serializers import TestReportSerializer, TestReportAdminSerializer


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


class TestReportAdminOrderingFilter(FilterSet):
    id = CharFilter(field_name='reportId')
    testReportInformationId__startTimestamp = CharFilter(
        field_name='testReportInformationId__startupTimestamp',
        label='Start Timestamp',
        lookup_expr='icontains'
    )
    testReportInformationId__endTimestamp = CharFilter(
        field_name='testReportInformationId__endTimestamp',
        label='End Timestamp',
        lookup_expr='icontains'
    )
    testReportInformationId__executionResult = CharFilter(
        field_name='testReportInformationId__executionResult',
        label='Execution Result',
        lookup_expr='icontains'
    )
    testReportInformationId__testDuration = CharFilter(
        field_name='testReportInformationId__testDuration',
        label='Test Duration',
        lookup_expr='icontains'
    )

    order_by_field = 'ordering'
    ordering = OrderingFilter(
        fields=(
            ('reportId', 'id'),
            ('testReportInformationId__startupTimestamp', 'testReportInformation.startupTimestamp'),
            ('testReportInformationId__endTimestamp', 'testReportInformation.endTimestamp'),
            ('testReportInformationId__executionResult', 'testReportInformation.executionResult'),
            ('testReportInformationId__testDuration', 'testReportInformation.testDuration')
        )
    )

    class Meta:
        model = TestReports
        fields = ['reportId']


class TestReportAdminModelViewSet(viewsets.ModelViewSet):
    """
    ModelViewSet that provides responses compatible with React Admin for TestReport objects.
    """
    queryset = TestReports.objects.all()
    serializer_class = TestReportAdminSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, ]
    filterset_fields = ['reportId', 'testId', 'testReportInformationId']
    filterset_class = TestReportAdminOrderingFilter
    pagination_class = ContentRangeHeaderPagination
