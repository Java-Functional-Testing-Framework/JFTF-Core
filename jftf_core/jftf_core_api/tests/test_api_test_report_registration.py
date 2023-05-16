from datetime import timedelta
from logging import getLogger
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from ..models import TestCases, TestReportInformation, TestCaseMetadata
from ..serializers import TestReportSerializer


class TestReportsSerializerTestCase(APITestCase):

    def user_authentication(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        # Log in the test user
        self.client = APIClient()
        self.client.login(username='testuser', password='testpassword')

    def setUp(self):
        self.test_logger = getLogger(f"Test logger {TestReportsSerializerTestCase.__name__}")
        self.user_authentication()
        # Create test data
        self.test_case_metadata = TestCaseMetadata.objects.create()
        self.test_case = TestCases.objects.create(metaDataId=self.test_case_metadata)
        self.test_case_metadata_2 = TestCaseMetadata.objects.create()
        self.test_case_2 = TestCases.objects.create(metaDataId=self.test_case_metadata_2)
        self.test_report_info = TestReportInformation.objects.create(testId=self.test_case,
                                                                     startupTimestamp=timezone.now(),
                                                                     endTimestamp=timezone.now(),
                                                                     testDuration="00:00:01")
        self.test_report_info_2 = TestReportInformation.objects.create(testId=self.test_case_2,
                                                                       startupTimestamp=timezone.now(),
                                                                       endTimestamp=timezone.now(),
                                                                       testDuration="00:00:01")
        self.valid_data = {
            'reportId': 1,
            'testId': self.test_case.testId,
            'testReportInformationId': self.test_report_info.testReportInformationId,
        }
        self.invalid_data = {
            'reportId': 2,
            'testId': self.test_case.testId,
            'testReportInformationId': self.test_report_info_2.testReportInformationId,  # Invalid testId
        }

    def test_valid_serializer_data(self):
        self.test_logger.info("Attempting valid test report registration")

        url = reverse('test-report-list')
        response = self.client.post(url, data=self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        serializer = TestReportSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_serializer_data(self):
        self.test_logger.info("Different embedded testId in TestReportInformation TestReportSerializer validation "
                              "checks")

        url = reverse('test-report-list')
        response = self.client.post(url, data=self.invalid_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)
        self.assertEqual(response.data['non_field_errors'][0],
                         "The testId in the linked testReportInformation object must match the current TestReports "
                         "object testId.")

        serializer = TestReportSerializer(data=self.invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('non_field_errors', serializer.errors)
        self.assertEqual(serializer.errors['non_field_errors'][0],
                         "The testId in the linked testReportInformation object must match the current TestReports "
                         "object testId.")
