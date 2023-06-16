from rest_framework import viewsets, permissions
from django_celery_results.models import TaskResult
from django_filters.rest_framework import DjangoFilterBackend
from ..serializers import TaskResultSerializer
from .pagination import ContentRangeHeaderPagination


class TaskResultViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TaskResult.objects.all()
    serializer_class = TaskResultSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['task_id']
    pagination_class = ContentRangeHeaderPagination
