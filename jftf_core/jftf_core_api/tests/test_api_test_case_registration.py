from logging import getLogger
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from ..models import TestCaseMetadata, TestCase


class TestCaseAPITestCase(APITestCase):

    def setUp(self):
        self.test_logger = getLogger(f"Test logger {TestCaseAPITestCase.__name__}")
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        # Log in the test user
        self.test_case_metadata_api_url = reverse('test-case-metadata-list')
        self.test_case_api_url = reverse('test-case-list')
        self.client = APIClient()
        self.client.login(username='testuser', password='testpassword')
        self.metadataId = 0

    def _create_test_metadata_helper(self):
        # Create a valid test case metadata object
        self.test_logger.info("Attempting to create valid test case metadata object")
        self.test_case_metadata = {
            "testName": "api_test",
            "featureGroup": "api_test",
            "testGroup": "api_test",
            "testPath": "/home/user/.jftf/test_cases/api_test/api_test/lib/api_test.jar",
            "testVersion": "1.0"
        }
        response = self.client.post(self.test_case_metadata_api_url, self.test_case_metadata, format='json')
        self.metadataId = response.data['metadataId']

        self.test_logger.info(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TestCaseMetadata.objects.count(), 1)
        self.assertEqual(TestCaseMetadata.objects.get().testName, "api_test")

    def Test_test_case_valid_registration(self):
        self.test_logger.info(f"Attempting test case registration for test case metadata id '{self.metadataId}'")
        self.test_case = {
            "firstExecution": "2023-05-03T18:03:14.029Z",
            "lastExecution": "2023-05-03T18:03:14.029Z",
            "executed": "true",
            "metaDataId": self.metadataId
        }
        response = self.client.post(self.test_case_api_url, self.test_case, format='json')

        self.test_logger.info(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TestCase.objects.count(), 1)
        self.assertEqual(TestCase.objects.get().metaDataId_id, self.metadataId)

    def Test_test_case_duplicate_metadata_registration(self):
        self.test_logger.info("Attempting test case duplicate test case metadata registration for "
                              f"test case metadata id '{self.metadataId}'")
        response = self.client.post(self.test_case_api_url, self.test_case, format='json')

        self.test_logger.info(response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(TestCase.objects.count(), 1)
        self.assertIn('non_field_errors', response.data.keys())
        self.assertEqual(response.data['non_field_errors'][0],
                         'A test case with this metadata id and name already exists.')

    def Test_test_case_invalid_test_case_metadata_pk(self):
        self.test_logger.info("Attempting test case registration for invalid test case metadata pk")
        self.test_case_invalid_test_case_metadata_pk = {
            "metaDataId": 100
        }
        response = self.client.post(self.test_case_api_url, self.test_case_invalid_test_case_metadata_pk, format='json')

        self.test_logger.info(response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(TestCase.objects.count(), 1)
        self.assertIn('metaDataId', response.data.keys())
        self.assertEqual(response.data['metaDataId'][0],
                         'Invalid pk \"100\" - object does not exist.')

    def Test_test_case_cascade_delete_check(self):
        self.test_logger.info("Verifying if test case entry is cascade deleted upon deleting linked "
                              "test case metadata entry")
        delete_test_case_metadata_url = f"{self.test_case_metadata_api_url}{self.metadataId}/"
        response = self.client.delete(delete_test_case_metadata_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(TestCaseMetadata.objects.count(), 0)
        self.assertEqual(TestCase.objects.count(), 0)

    def test_api_test_case_registration(self):
        self._create_test_metadata_helper()
        self.test_logger.info(f"Generated test case metadataId is '{self.metadataId}'")
        self.Test_test_case_valid_registration()
        self.Test_test_case_duplicate_metadata_registration()
        self.Test_test_case_invalid_test_case_metadata_pk()
        self.Test_test_case_cascade_delete_check()
