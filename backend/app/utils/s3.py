"""AWS S3 upload/download helpers for PDF reports."""

import boto3
from app.config import get_settings

settings = get_settings()


def get_s3_client():
    return boto3.client(
        "s3",
        region_name=settings.AWS_REGION,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    )


def upload_pdf(key: str, body: bytes) -> str:
    """Upload a PDF to S3 and return the URL."""
    client = get_s3_client()
    client.put_object(
        Bucket=settings.AWS_S3_BUCKET,
        Key=key,
        Body=body,
        ContentType="application/pdf",
    )
    return f"https://{settings.AWS_S3_BUCKET}.s3.{settings.AWS_REGION}.amazonaws.com/{key}"


def get_presigned_url(key: str, expires_in: int = 3600) -> str:
    """Generate a pre-signed download URL."""
    client = get_s3_client()
    return client.generate_presigned_url(
        "get_object",
        Params={"Bucket": settings.AWS_S3_BUCKET, "Key": key},
        ExpiresIn=expires_in,
    )
