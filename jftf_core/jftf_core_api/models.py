from django.db import models


# Metaclass added for each model for old JftfDetachedRunner compatibility
class TestCaseMetadata(models.Model):
    metadataId = models.AutoField(primary_key=True)
    testName = models.CharField(max_length=255)
    featureGroup = models.CharField(max_length=255, null=True, blank=True)
    testGroup = models.CharField(max_length=255)
    testPath = models.CharField(max_length=512)
    testVersion = models.CharField(max_length=255)

    class Meta:
        db_table = "TestCaseMetadata"


class TestCases(models.Model):
    testId = models.AutoField(primary_key=True)
    metaDataId = models.ForeignKey(TestCaseMetadata, on_delete=models.CASCADE, db_column="metaDataId")
    firstExecution = models.DateTimeField(null=True, blank=True)
    lastExecution = models.DateTimeField(null=True, blank=True)
    executed = models.BooleanField(default=False)

    class Meta:
        db_table = "TestCases"


class TestReportInformation(models.Model):
    testReportInformationId = models.AutoField(primary_key=True)
    testId = models.ForeignKey(TestCases, on_delete=models.CASCADE, db_column="testId")
    startupTimestamp = models.DateTimeField(auto_now_add=True)
    endTimestamp = models.DateTimeField(auto_now_add=True)
    testDuration = models.TimeField()
    errorMessages = models.TextField(null=True, blank=True)
    loggerOutput = models.TextField(null=True, blank=True)
    executionResult = models.CharField(max_length=255)

    class Meta:
        db_table = "TestReportInformation"


class TestReports(models.Model):
    reportId = models.AutoField(primary_key=True)
    testId = models.ForeignKey(TestCases, on_delete=models.CASCADE, db_column="testId")
    testReportInformationId = models.ForeignKey(TestReportInformation, on_delete=models.CASCADE,
                                                db_column="testReportInformationId")

    class Meta:
        db_table = "TestReports"
