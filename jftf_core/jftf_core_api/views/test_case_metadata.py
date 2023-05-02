from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from ..models import TestCaseMetadata
from ..serializers import TestCaseMetadataSerializer


class TestCaseMetadataModelViewSet(LoginRequiredMixin, viewsets.ModelViewSet):
    """
    ModelViewSet for CRUD operations on TestCaseMetadata objects.
    """
    queryset = TestCaseMetadata.objects.all()
    serializer_class = TestCaseMetadataSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['testName', 'testGroup', 'featureGroup']
