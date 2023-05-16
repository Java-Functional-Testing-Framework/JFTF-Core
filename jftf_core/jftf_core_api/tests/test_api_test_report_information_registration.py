from logging import getLogger
from copy import deepcopy
from django.urls import reverse
from rest_framework import status
from datetime import datetime
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from ..models import TestReportInformation, TestCases, TestCaseMetadata


class TestReportInformationAPITestCase(APITestCase):
    def setUp(self):
        self.test_logger = getLogger(f"Test logger {TestReportInformationAPITestCase.__name__}")
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        # Log in the test user
        self.test_case_metadata_api_url = reverse('test-case-metadata-list')
        self.test_case_api_url = reverse('test-case-list')
        self.client = APIClient()
        self.client.login(username='testuser', password='testpassword')
        self.test_report_information_api_url = reverse('test-report-information-list')
        self.test_report_information_data = {
            'testId': 0,
            'startupTimestamp': datetime(2023, 5, 1, 12, 0, 0),
            'endTimestamp': datetime(2023, 5, 2, 12, 0, 0),
            'testDuration': '00:30:00',
            'errorMessages': 'Some error messages',
            'loggerOutput': 'Logger output',
            'executionResult': 'successfulState',
        }

    def Test_create_valid_test_report_information(self):
        self.test_logger.info("Attempting valid test report information registration")

        self.test_logger.info("Mocking an existing TestCase entry")
        mock_test_case_metadata = TestCaseMetadata.objects.create()
        mock_test_case_id = TestCases.objects.create(metaDataId=mock_test_case_metadata).testId
        self.test_report_information_data['testId'] = mock_test_case_id
        self.test_logger.info("Creating valid TestReportInformation associated with testId "
                              f"'{self.test_report_information_data['testId']}'")
        response = self.client.post(self.test_report_information_api_url, self.test_report_information_data)

        self.test_logger.info(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TestReportInformation.objects.count(), 1)
        self.assertEqual(response.data['testId'], mock_test_case_id)

    def Test_end_timestamp_before(self):
        self.test_logger.info("Attempting invalid test report information registration with end timestamp "
                              "coming before start timestamp")

        self.invalid_test_data = deepcopy(self.test_report_information_data)
        self.invalid_test_data['endTimestamp'] = datetime(2023, 4, 1, 12, 0, 0)
        response = self.client.post(self.test_report_information_api_url, self.invalid_test_data)

        self.test_logger.info(response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data.keys())
        self.assertEqual(response.data['non_field_errors'][0],
                         'End timestamp cannot be before the start timestamp.')

    def Test_invalid_test_execution_result_identifier(self):
        self.test_logger.info("Attempting invalid test report information registration with invalid "
                              "execution result identifier")

        self.invalid_test_data = deepcopy(self.test_report_information_data)
        self.invalid_test_data['executionResult'] = "invalidResult"
        response = self.client.post(self.test_report_information_api_url, self.invalid_test_data)

        self.test_logger.info(response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data.keys())
        self.assertEqual(response.data['non_field_errors'][0],
                         'Invalid value for executionResult. Only \'successfulState\' and \'errorState\' are allowed.')

    def test_api_report_information(self):
        self.Test_create_valid_test_report_information()
        self.Test_end_timestamp_before()
        self.Test_invalid_test_execution_result_identifier()
