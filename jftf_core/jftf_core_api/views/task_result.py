from rest_framework import viewsets
from django_celery_results.models import TaskResult
from ..serializers import TaskResultSerializer
from .pagination import ContentRangeHeaderPagination


class TaskResultViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TaskResult.objects.all()
    serializer_class = TaskResultSerializer
    pagination_class = ContentRangeHeaderPagination
    filterset_fields = ['task_id']
