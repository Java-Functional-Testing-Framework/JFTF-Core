from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from ..models import TestCases, TestCaseMetadata
from django.contrib.auth.models import User


class ExecuteMultipleTestCase(APITestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create an authenticated client
        self.client = APIClient()
        self.client.login(username='testuser', password='testpassword')

        # Create some test cases
        self.test_case_metadata_1 = TestCaseMetadata.objects.create()
        self.test_case_1 = TestCases.objects.create(metaDataId=self.test_case_metadata_1)
        self.test_case_metadata_2 = TestCaseMetadata.objects.create()
        self.test_case_2 = TestCases.objects.create(metaDataId=self.test_case_metadata_2)
        self.test_case_metadata_3 = TestCaseMetadata.objects.create()
        self.test_case_3 = TestCases.objects.create(metaDataId=self.test_case_metadata_3)

    def test_execute_multiple_route_with_valid_body(self):
        # Prepare the request payload with valid runner and test_case_ids
        payload = {
            'runner': 'JftfDetachedRunner',
            'test_case_ids': [self.test_case_1.pk, self.test_case_2.pk, self.test_case_3.pk]
        }

        # Make a POST request to the execute_multiple route
        url = reverse('test-case-execute-multiple')
        response = self.client.post(url, data=payload, format='json')

        # Assert that the response status code is 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the response contains the task ID
        self.assertIn('task_id', response.data)

    def test_execute_multiple_route_with_missing_runner(self):
        # Prepare the request payload without the runner parameter
        payload = {
            'test_case_ids': [self.test_case_1.pk, self.test_case_2.pk, self.test_case_3.pk]
        }

        # Make a POST request to the execute_multiple route
        url = reverse('test-case-execute-multiple')
        response = self.client.post(url, data=payload, format='json')

        # Assert that the response status code is 400
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Assert that the response contains the error message
        self.assertIn('Missing "runner" parameter', response.data['error'])

    def test_execute_multiple_route_with_missing_test_case_ids(self):
        # Prepare the request payload without the test_case_ids parameter
        payload = {
            'runner': 'JftfDetachedRunner'
        }

        # Make a POST request to the execute_multiple route
        url = reverse('test-case-execute-multiple')
        response = self.client.post(url, data=payload, format='json')

        # Assert that the response status code is 400
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Assert that the response contains the error message
        self.assertIn('Missing "test_case_ids" parameter', response.data['error'])

    def test_execute_multiple_route_with_invalid_runner(self):
        # Prepare the request payload with an invalid runner value
        payload = {
            'runner': 'invalid_runner',
            'test_case_ids': [self.test_case_1.pk, self.test_case_2.pk, self.test_case_3.pk]
        }

        # Make a POST request to the execute_multiple route
        url = reverse('test-case-execute-multiple')
        response = self.client.post(url, data=payload, format='json')

        # Assert that the response status code is 400
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Assert that the response contains the error message
        self.assertIn('Invalid test runner', response.data['error'])

    def test_execute_multiple_route_with_nonexistent_test_case(self):
        # Prepare the request payload with a non-existent test_case_id
        payload = {
            'runner': 'JftfDetachedRunner',
            'test_case_ids': [99999]  # Non-existent test_case_id
        }

        # Make a POST request to the execute_multiple route
        url = reverse('test-case-execute-multiple')
        response = self.client.post(url, data=payload, format='json')

        # Assert that the response status code is 404
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Assert that the response contains the error message
        self.assertIn('TestCase with ID 99999 does not exist', response.data['error'])
