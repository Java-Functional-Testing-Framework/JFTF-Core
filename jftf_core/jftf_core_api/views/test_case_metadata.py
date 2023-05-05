from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from .pagination import ContentRangeHeaderPagination
from ..models import TestCaseMetadata
from ..serializers import TestCaseMetadataSerializer


class TestCaseMetadataModelViewSet(viewsets.ModelViewSet):
    """
    ModelViewSet for CRUD operations on TestCaseMetadata objects.
    """
    queryset = TestCaseMetadata.objects.all()
    serializer_class = TestCaseMetadataSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['testName', 'testGroup', 'featureGroup']
    pagination_class = ContentRangeHeaderPagination
