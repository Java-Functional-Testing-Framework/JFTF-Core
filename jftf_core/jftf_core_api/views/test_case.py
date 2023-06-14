from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
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
    filterset_fields = ['executed']
    pagination_class = ContentRangeHeaderPagination

    @extend_schema(
        description='Execute the TestCase',
        responses={
            200: {'description': 'Task ID of the executed TestCase', 'content': {
                'application/json': {'schema': {'type': 'object', 'properties': {'task_id': {'type': 'string'}}}}}},
            404: {'description': 'TestCase not found', 'content': {
                'application/json': {'schema': {'type': 'object', 'properties': {'error': {'type': 'string'}}}}}},
            500: {'description': 'Internal server error', 'content': {
                'application/json': {'schema': {'type': 'object', 'properties': {'error': {'type': 'string'}}}}}}
        }
    )
    @action(detail=True, methods=['post'])
    def execute(self, request, pk=None):
        try:
            # Retrieve the TestCase instance
            test_case = self.get_object()

            # Serialize the TestCase instance
            serializer = self.get_serializer(test_case)
            serialized_data = serializer.data

            # Access the metaData field value from the serialized data
            metaData_value = serialized_data['metaData']

            # Get the jar path from the metaData serialized data
            jar_path = metaData_value['testPath']

            # Trigger the celery task
            result = execute_jftf_test_case.delay(jar_path)

            # Return the task ID or any other response as needed
            return Response({'task_id': result.id}, status=status.HTTP_200_OK)
        except TestCases.DoesNotExist:
            return Response({'error': 'TestCase not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TestCaseAdminModelViewSet(viewsets.ModelViewSet):
    """
    ModelViewSet that provides responses compatible with React Admin for TestCase objects.
    """
    queryset = TestCases.objects.all()
    serializer_class = TestCaseAdminSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['executed']
    pagination_class = ContentRangeHeaderPagination
