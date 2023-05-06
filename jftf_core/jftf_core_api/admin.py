from django.contrib import admin
from .models import TestCaseMetadata, TestCases, TestReportInformation, TestReports

admin.site.register(TestCaseMetadata)
admin.site.register(TestCases)
admin.site.register(TestReportInformation)
admin.site.register(TestReports)
