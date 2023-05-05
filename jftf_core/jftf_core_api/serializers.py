from re import match
from rest_framework import serializers
from .models import TestCaseMetadata, TestCase


class TestCaseMetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCaseMetadata
        fields = '__all__'

    def validate(self, data):
        # Check if another entry exists in the database with the same test version, test path, and test name
        test_version = data.get('testVersion')
        test_path = data.get('testPath')
        test_name = data.get('testName')

        existing_entry = TestCaseMetadata.objects.filter(testVersion=test_version, testPath=test_path,
                                                         testName=test_name).exists()

        if existing_entry:
            raise serializers.ValidationError(
                "Duplicate entry with the same test version, test path, and test name already exists")

        # Check if the test path is valid and formatted correctly
        valid_path_pattern = r'^\/home\/[\w-]+\/\.jftf\/test_cases\/([\w-]+)\/([\w-]+)\/lib\/\2\.jar$'
        re_match = match(valid_path_pattern, test_path)

        if not re_match:
            raise serializers.ValidationError(
                "Invalid test case path. "
                "The correct format is /home/<username>/.jftf/test_cases/(testgroup)/(testname)/lib/(testname).jar")

        # Extract test group and test name from the matched pattern
        path_test_group = re_match.group(1)
        path_test_name = re_match.group(2)

        # Check if the test group and test name from the path match the provided values
        if data.get('testGroup') != path_test_group or data.get('testName') != path_test_name:
            raise serializers.ValidationError(
                "The test group and(/)or test name in the test path do not correspond with the provided values")

        return data


class TestCaseSerializer(serializers.ModelSerializer):
    metaData = serializers.SerializerMethodField()

    class Meta:
        model = TestCase
        fields = '__all__'

    def validate(self, data):
        if self.instance is not None:
            # In case of a PUT method, instance already exists, it is the current TestCase entry,
            # so exclude in the filter the current testId
            # however, still check against other metadataId linked to other TestCase entries
            queryset = TestCase.objects.filter(metaDataId=data['metaDataId']).exclude(testId=self.instance.testId)
            if queryset.exists():
                raise serializers.ValidationError('A test case with this metadata id and name already exists.')
        else:
            # Check if there are any other test cases with the same metadata id and name
            queryset = TestCase.objects.filter(metaDataId=data['metaDataId'])
            if queryset.exists():
                raise serializers.ValidationError('A test case with this metadata id and name already exists.')

        return data

    def get_metaData(self, obj):
        metaData = obj.metaDataId
        return TestCaseMetadataSerializer(metaData).data


class TestCaseAdminSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='testId')
    metaData = serializers.SerializerMethodField()

    class Meta:
        model = TestCase
        fields = ['id', 'firstExecution', 'lastExecution', 'executed', 'metaData']

    def get_metaData(self, obj):
        metaData = obj.metaDataId
        return TestCaseMetadataSerializer(metaData).data
