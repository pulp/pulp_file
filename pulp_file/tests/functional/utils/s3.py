import boto3
import botocore
from django.conf import settings


BUCKET_NAME = getattr(settings, "AWS_STORAGE_BUCKET_NAME", "")


def s3_settings():
    """Generate S3 settings."""
    config = boto3.session.Config(
        retries={"total_max_attempts": 10},
        signature_version=settings.AWS_S3_SIGNATURE_VERSION,
        region_name=settings.AWS_S3_REGION_NAME,
        s3={"addressing_style": settings.AWS_S3_ADDRESSING_STYLE},
    )
    return dict(
        service_name="s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME,
        endpoint_url=settings.AWS_S3_ENDPOINT_URL,
        config=config,
    )


def bucket_exists(bucket_name=BUCKET_NAME):
    """Test if bucket exists."""
    s3 = boto3.resource(**s3_settings())
    exists = True
    try:
        s3.meta.client.head_bucket(Bucket=bucket_name)
    except botocore.exceptions.ClientError as e:
        # If a client error is thrown, then check that it was a 404 error.
        # If it was a 404 error, then the bucket does not exist.
        error_code = e.response["Error"]["Code"]
        if error_code != "404":
            raise
        exists = False

    return exists


def create_bucket(bucket_name=BUCKET_NAME):
    """Create bucket if needed."""
    s3_test = "S3Boto3Storage" in settings.DEFAULT_FILE_STORAGE
    if s3_test and not bucket_exists(bucket_name=bucket_name):
        session = boto3.session.Session()
        s3 = session.resource(**s3_settings())
        bucket = s3.Bucket(bucket_name)
        bucket.create()
