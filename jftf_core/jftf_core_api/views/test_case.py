from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django_filters.filters import OrderingFilter, CharFilter
from django_filters import FilterSet
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from django.conf import settings
from ..tasks import execute_jftf_test_case
from .pagination import ContentRangeHeaderPagination
from ..models import TestCases
from ..serializers import TestCaseSerializer, TestCaseAdminSerializer


class TestCaseModelViewSet(viewsets.ModelViewSet):
    """
    ModelViewSet for CRUD operations on TestCase objects.
    """
    queryset = TestCases.objects.all()
    serializer_class = TestCaseSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['executed', 'metaDataId']
    pagination_class = None

    @extend_schema(
        description='Execute the TestCase',
        responses={
            200: {'description': 'Task ID of the executed TestCase', 'content': {
                'application/json': {'schema': {'type': 'object', 'properties': {'task_id': {'type': 'string'}}}}}},
            400: {'description': 'Bad request', 'content': {
                'application/json': {'schema': {'type': 'object', 'properties': {'error': {'type': 'string'}}}}}},
            404: {'description': 'TestCase not found', 'content': {
                'application/json': {'schema': {'type': 'object', 'properties': {'error': {'type': 'string'}}}}}},
            500: {'description': 'Internal server error', 'content': {
                'application/json': {'schema': {'type': 'object', 'properties': {'error': {'type': 'string'}}}}}}
        },
        request={'application/json': {'schema': {'type': 'object', 'properties': {'runner': {'type': 'string'}}}}}
    )
    @action(detail=True, methods=['post'])
    def execute(self, request, pk=None):
        try:
            # Check if the runner parameter is present in the request body
            if 'runner' not in request.data:
                return Response({'error': 'Missing "runner" parameter from JSON request body'},
                                status=status.HTTP_400_BAD_REQUEST)

            # Retrieve the TestCase instance
            test_case = self.get_object()

            # Get the runner from the request body
            runner = request.data['runner']

            # Check if the runner is valid
            if runner not in settings.JFTF_AVAILABLE_RUNNERS:
                return Response({'error': 'Invalid test runner'}, status=status.HTTP_400_BAD_REQUEST)

            # Serialize the TestCase instance
            serializer = self.get_serializer(test_case)
            serialized_data = serializer.data

            # Access the metaData field value from the serialized data
            metaData_value = serialized_data['metaData']

            # Get the jar path from the metaData serialized data
            jar_path = metaData_value['testPath']

            # Trigger the celery task
            result = execute_jftf_test_case.delay(jar_path, runner)

            # Return the task ID or any other response as needed
            return Response({'task_id': result.id}, status=status.HTTP_200_OK)
        except TestCases.DoesNotExist:
            return Response({'error': 'TestCase not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TestCaseAdminOrderingFilter(FilterSet):
    id = CharFilter(field_name='testId')

    order_by_field = 'ordering'
    ordering = OrderingFilter(
        fields=(
            ('testId', 'id'),
            ('executed', 'executed'),
            ('firstExecution', 'firstExecution'),
            ('lastExecution', 'lastExecution'),
        )
    )

    class Meta:
        model = TestCases
        fields = ['testId', 'executed', 'firstExecution', 'lastExecution']


class TestCaseAdminModelViewSet(viewsets.ModelViewSet):
    """
    ModelViewSet that provides responses compatible with React Admin for TestCase objects.
    """
    queryset = TestCases.objects.all()
    serializer_class = TestCaseAdminSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, ]
    filterset_fields = ['executed']
    filterset_class = TestCaseAdminOrderingFilter
    pagination_class = ContentRangeHeaderPagination
