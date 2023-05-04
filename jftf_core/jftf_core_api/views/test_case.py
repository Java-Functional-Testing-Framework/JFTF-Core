from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from ..models import TestCase
from ..serializers import TestCaseSerializer


class TestCaseModelViewSet(viewsets.ModelViewSet):
    """
    ModelViewSet for CRUD operations on TestCase objects.
    """
    queryset = TestCase.objects.all()
    serializer_class = TestCaseSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['executed']
