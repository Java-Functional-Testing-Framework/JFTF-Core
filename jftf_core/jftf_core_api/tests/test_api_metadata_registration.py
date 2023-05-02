from logging import getLogger
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from ..models import TestCaseMetadata
from django.contrib.auth.models import User


class TestCaseMetadataAPITestCase(APITestCase):

    def setUp(self):
        self.test_logger = getLogger(f"Test logger {TestCaseMetadataAPITestCase.__name__}")
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        # Log in the test user
        self.client = APIClient()
        self.client.login(username='testuser', password='testpassword')
        self.duplicate_metadata = {
            "testName": "test1",
            "featureGroup": "feature1",
            "testGroup": "group1",
            "testPath": "/home/user/.jftf/test_cases/group1/test1/lib/test1.jar",
            "testVersion": "1.0"
        }

    def Test_create_test_case_metadata(self):
        # Create a valid test case metadata object
        self.test_logger.info("Attempting to create valid test case metadata object")
        url = reverse('test-case-metadata-list')
        response = self.client.post(url, self.duplicate_metadata, format='json')

        self.test_logger.info(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TestCaseMetadata.objects.count(), 1)
        self.assertEqual(TestCaseMetadata.objects.get().testName, "test1")

    def Test_create_test_case_metadata_duplicate_entry(self):
        self.test_logger.info("Test case metadata duplicate entry test")
        url = reverse('test-case-metadata-list')
        response = self.client.post(url, self.duplicate_metadata, format='json')

        self.test_logger.info(response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'non_field_errors': [
            'Duplicate entry with the same test version, test path, and test name already exists']})

    def Test_create_test_case_metadata_invalid_test_path(self):
        # Attempt to create a test case metadata object with an invalid test path
        self.test_logger.info("Test case metadata with invalid test path")
        data = {
            "testName": "test1",
            "featureGroup": "feature1",
            "testGroup": "group1",
            "testPath": "/invalid/test_path/test1.jar",
            "testVersion": "1.0"
        }

        url = reverse('test-case-metadata-list')
        response = self.client.post(url, data, format='json')

        self.test_logger.info(response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data.keys())
        self.assertEqual(response.data['non_field_errors'][0],
                         'Invalid test case path. The correct format is /home/<username>/.jftf/test_cases/('
                         'testgroup)/(testname)/lib/(testname).jar')

    def Test_create_test_case_metadata_invalid_test_group_and_test_name(self):
        # Attempt to create a test case metadata object with test group and test name that do not correspond
        # to the provided values
        self.test_logger.info("Test case metadata with invalid group and test name")
        data = {
            "testName": "test2",
            "featureGroup": "feature1",
            "testGroup": "group1",
            "testPath": "/home/user/.jftf/test_cases/group1/test1/lib/test1.jar",
            "testVersion": "1.0"
        }

        url = reverse('test-case-metadata-list')
        response = self.client.post(url, data, format='json')

        self.test_logger.info(response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data.keys())
        self.assertEqual(response.data['non_field_errors'][0],
                         'The test group and(/)or test name in the test path do not correspond with the '
                         'provided values')

    def test_api_metadata_creation(self):
        self.Test_create_test_case_metadata()
        self.Test_create_test_case_metadata_duplicate_entry()
        self.Test_create_test_case_metadata_invalid_test_path()
        self.Test_create_test_case_metadata_invalid_test_group_and_test_name()
