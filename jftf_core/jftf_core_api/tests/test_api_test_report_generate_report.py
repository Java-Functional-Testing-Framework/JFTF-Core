from datetime import datetime
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from ..models import TestReports, TestReportInformation, TestCases, TestCaseMetadata
from django.contrib.auth.models import User


class GenerateTestReportTestCase(APITestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create an authenticated client
        self.client = APIClient()
        self.client.login(username='testuser', password='testpassword')

        # Create a test report
        self.test_case_metadata = TestCaseMetadata.objects.create()
        self.test_case = TestCases.objects.create(metaDataId=self.test_case_metadata)
        self.test_report_information = TestReportInformation.objects.create(
            testId=self.test_case,
            startupTimestamp=datetime(2023, 6, 22, 12, 0, 0),
            endTimestamp=datetime(2023, 6, 22, 12, 0, 0),
            testDuration=datetime.min.time(),
            errorMessages="Some error messages",
            loggerOutput="Logger output",
            executionResult="successfulState"
        )
        self.test_report = TestReports.objects.create(testId=self.test_case,
                                                      testReportInformationId=self.test_report_information)

    def test_generate_report_route_with_valid_report_id(self):
        # Make a GET request to the generate_report route
        url = reverse('test-report-generate-report', kwargs={'pk': self.test_report.pk})
        response = self.client.get(url)

        # Assert that the response status code is 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the response contains the file content
        self.assertTrue(response.streaming_content)

        # Assert that the response contains the appropriate Content-Disposition header
        self.assertIn('attachment; filename=test_report_', response.get('Content-Disposition'))

    def test_generate_report_route_with_invalid_report_id(self):
        # Make a GET request to the generate_report route with an invalid report_id
        url = reverse('test-report-generate-report', kwargs={'pk': 99999})  # Non-existent report_id
        response = self.client.get(url)

        # Assert that the response status code is 404
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Assert that the response contains the error message
        self.assertIn('Not found', response.data['detail'])
