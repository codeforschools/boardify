import os

import boto3


def get_bucket(bucket=None):
    bucket = bucket or os.environ.get("AWS_S3_BUCKET")
    if not bucket:
        raise SystemExit("AWS_S3_BUCKET is not set (the bucket PDFs are uploaded to).")
    return bucket


def get_client():
    """
    S3 client. AWS_S3_ACCESS_KEY / AWS_S3_SECRET_KEY are used when both are set;
    otherwise boto3's default credential chain applies (an OIDC role in CI, an AWS
    profile locally), so no long-lived keys are required.
    """
    kwargs = {"region_name": os.environ.get("AWS_S3_REGION") or None}
    access_key = os.environ.get("AWS_S3_ACCESS_KEY")
    secret_key = os.environ.get("AWS_S3_SECRET_KEY")
    if access_key and secret_key:
        kwargs.update(aws_access_key_id=access_key, aws_secret_access_key=secret_key)
    return boto3.client("s3", **kwargs)


def upload_file(filepath, key=None, bucket=None):
    """
    Upload a local PDF to S3, returning the object key it was stored under
    """
    key = key or filepath.rpartition("/")[2]
    get_client().upload_file(
        filepath, get_bucket(bucket), key, ExtraArgs={"ContentType": "application/pdf"}
    )
    return key


def delete_file(key, bucket=None):
    """
    Delete an object from S3
    """
    get_client().delete_object(Bucket=get_bucket(bucket), Key=key)
    return key
