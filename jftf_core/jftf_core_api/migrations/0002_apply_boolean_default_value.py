# Generated by Django 4.2 on 2023-04-03 13:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jftf_core_api', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL('ALTER TABLE TestCases MODIFY executed BOOLEAN NOT NULL DEFAULT FALSE;'),
    ]