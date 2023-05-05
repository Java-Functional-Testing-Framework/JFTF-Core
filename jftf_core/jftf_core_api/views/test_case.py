from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from .pagination import ContentRangeHeaderPagination
from ..models import TestCase
from ..serializers import TestCaseSerializer, TestCaseAdminSerializer


class TestCaseModelViewSet(viewsets.ModelViewSet):
    """
    ModelViewSet for CRUD operations on TestCase objects.
    """
    queryset = TestCase.objects.all()
    serializer_class = TestCaseSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['executed']
    pagination_class = ContentRangeHeaderPagination


class TestCaseAdminModelViewSet(viewsets.ModelViewSet):
    """
    ModelViewSet that provides responses compatible with React Admin.
    """
    queryset = TestCase.objects.all()
    serializer_class = TestCaseAdminSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['executed']
    pagination_class = ContentRangeHeaderPagination
    
