from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from ..serializers import TestCaseMetadataSerializer


class TestCaseMetadataRegistrationViewSet(LoginRequiredMixin, viewsets.ViewSet):
    """
    ViewSet for TestCaseMetadata model.
    """

    @extend_schema(
        request=TestCaseMetadataSerializer,
        responses={201: TestCaseMetadataSerializer},
        description='Gather test case metadata and create a new TestCaseMetadata object.'
    )
    def create(self, request):
        serializer = TestCaseMetadataSerializer(data=request.data)
        if serializer.is_valid():
            test_case_metadata = serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
