"""Defines the location for AWS static files storage."""
from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    """Provide access to the AWS storage location for static files."""

    location = settings.STATICFILES_LOCATION
