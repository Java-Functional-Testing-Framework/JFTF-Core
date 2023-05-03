from django.contrib import admin
from .models import TestCaseMetadata, TestCase, TestReportInformation, TestReports

admin.site.register(TestCaseMetadata)
admin.site.register(TestCase)
admin.site.register(TestReportInformation)
admin.site.register(TestReports)
