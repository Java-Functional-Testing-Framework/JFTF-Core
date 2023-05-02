from django.contrib import admin
from .models import TestCaseMetadata, TestCase

admin.site.register(TestCaseMetadata)
admin.site.register(TestCase)
