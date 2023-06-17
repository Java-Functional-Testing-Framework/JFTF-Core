from typing import Union
from drf_spectacular.utils import extend_schema
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .pagination import ContentRangeHeaderPagination
from ..models import TestCaseMetadata
from ..serializers import TestCaseMetadataSerializer


def check_registration_status(validated_serializer: TestCaseMetadataSerializer) -> Union[bool, None]:
    if validated_serializer.errors:
        if validated_serializer.errors['non_field_errors'][0] == "Duplicate entry with the same test version, test " \
                                                                 "path, and test name already exists":
            return True
        else:
            return None
    else:
        return False


class TestCaseMetadataModelViewSet(viewsets.ModelViewSet):
    """
    ModelViewSet for CRUD operations on TestCaseMetadata objects.
    """
    queryset = TestCaseMetadata.objects.all()
    serializer_class = TestCaseMetadataSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['testName', 'testGroup', 'featureGroup', 'testPath', 'testVersion']
    pagination_class = ContentRangeHeaderPagination

    @extend_schema(
        description='Check registration status for a test application based on the provided test case metadata '
                    'information.'
    )
    @action(detail=False, methods=['post'])
    def check_registration_status(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()

        is_registered = check_registration_status(serializer)
        if is_registered is True:
            feedback_message = "The test case is registered."
        elif is_registered is False:
            feedback_message = "The test case is not registered."
        else:
            feedback_message = "Registration status is inconclusive."

        feedback = {
            'is_registered': is_registered,
            'message': feedback_message,
            'serializer_errors': serializer.errors
        }

        return Response(feedback, status=status.HTTP_200_OK)
