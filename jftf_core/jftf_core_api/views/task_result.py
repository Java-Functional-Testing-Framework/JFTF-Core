from rest_framework import viewsets, permissions
from django_celery_results.models import TaskResult
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..serializers import TaskResultSerializer
from .pagination import ContentRangeHeaderPagination


class TaskResultViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ReadOnlyModelViewSet for CRUD read-only operations on TaskResult objects.
    """
    queryset = TaskResult.objects.all()
    serializer_class = TaskResultSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['task_id']
    pagination_class = None


class TaskResultAdminViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ReadOnlyModelViewSet that provides responses compatible with React Admin for TaskResult objects.
    """
    queryset = TaskResult.objects.all()
    serializer_class = TaskResultSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['task_id']
    ordering_fields = ['id', 'status']
    pagination_class = ContentRangeHeaderPagination
