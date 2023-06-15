from django.urls import reverse
from logging import getLogger
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from ..models import TestCases, TestCaseMetadata
from django.contrib.auth.models import User


class ExecuteTestCase(APITestCase):
    def setUp(self):
        self.test_logger = getLogger(f"Test logger {ExecuteTestCase.__name__}")

        # Create a TestCaseMetadata object
        self.metadata = TestCaseMetadata.objects.create(
            testName='Test Case 1',
            featureGroup='Feature Group 1',
            testGroup='Test Group 1',
            testPath='/path/to/test_case',
            testVersion='1.0'
        )

        # Create a TestCases object
        self.test_case = TestCases.objects.create(metaDataId=self.metadata)

        # Create test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create an authenticated client

        self.client = APIClient()
        self.client.login(username='testuser', password='testpassword')

    def test_execute_route_with_valid_body(self):
        # Prepare the request payload with a valid runner value
        payload = {'runner': 'JftfDetachedRunner'}

        # Make a POST request to the execute route
        url = reverse('test-case-execute', kwargs={'pk': self.test_case.pk})
        response = self.client.post(url, data=payload, format='json')

        # Assert that the response status code is 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the response contains the task ID
        self.assertIn('task_id', response.data)

    def test_execute_route_with_missing_runner(self):
        # Prepare the request payload without the runner parameter
        payload = {}

        # Make a POST request to the execute route
        url = reverse('test-case-execute', kwargs={'pk': self.test_case.pk})
        response = self.client.post(url, data=payload, format='json')

        # Assert that the response status code is 400
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Assert that the response contains the error message
        self.assertIn('Missing "runner" parameter', response.data['error'])

    def test_execute_route_with_invalid_runner(self):
        # Prepare the request payload with an invalid runner value
        payload = {'runner': 'invalid_runner'}

        # Make a POST request to the execute route
        url = reverse('test-case-execute', kwargs={'pk': self.test_case.pk})
        response = self.client.post(url, data=payload, format='json')

        # Assert that the response status code is 400
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Assert that the response contains the error message
        self.assertIn('Invalid test runner', response.data['error'])
