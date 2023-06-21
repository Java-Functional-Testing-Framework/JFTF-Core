from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from django.template import loader
from django.http import FileResponse
from django_filters.filters import OrderingFilter, CharFilter
from django_filters import FilterSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from drf_spectacular.utils import extend_schema
from .pagination import ContentRangeHeaderPagination
from ..models import TestReports, TestCases
from ..serializers import TestReportSerializer, TestReportAdminSerializer, TestCaseSerializer


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

    @extend_schema(
        description='Generate a test report',
        responses={
            200: {
                'description': 'Test report file',
                'content': {
                    'text/html': {}
                }
            }
        }
    )
    @action(detail=True, methods=['get'])
    def generate_report(self, request, pk=None):
        # Retrieve the test report object
        test_report = self.get_object()

        # Serialize the test report object
        serializer = self.get_serializer(test_report)
        serialized_data = serializer.data

        # Get the test report information from the serialized data
        test_report_information = serialized_data['testReportInformation']

        # Retrieve the associated test object
        test_id = test_report_information['testId']
        test = TestCases.objects.get(pk=test_id)

        # Serialize the test object
        test_serializer = TestCaseSerializer(test)
        test_metadata = test_serializer.data['metaData']

        # Render the test report template
        template = loader.get_template('report/test_report_dark_theme.html')
        context = {
            'test_report_information': test_report_information,
            'test_metadata': test_metadata
        }
        rendered_report = template.render(context)

        # Generate and return the report file
        response = FileResponse(
            rendered_report,
            content_type='text/html'
        )
        response['Content-Disposition'] = f'attachment; filename=test_report_{test_metadata["testName"]}_Id_{pk}.html'
        return response


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
    filter_backends = [DjangoFilterBackend, SearchFilter, ]
    filterset_fields = ['reportId', 'testId', 'testReportInformationId']
    filterset_class = TestReportAdminOrderingFilter
    search_fields = ['testId__metaDataId__testName', 'testReportInformationId__executionResult']
    pagination_class = ContentRangeHeaderPagination
