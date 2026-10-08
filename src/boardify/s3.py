import os

import boto3


def get_client():
    """
    Set up the S3 client using credentials from the environment
    """
    client = boto3.client(
        "s3",
        aws_access_key_id=os.environ["AWS_S3_ACCESS_KEY"],
        aws_secret_access_key=os.environ["AWS_S3_SECRET_KEY"],
        region_name=os.environ.get("AWS_S3_REGION"),
    )
    return client


def upload_file(filepath, key=None, bucket=None):
    """
    Upload a local file to S3, returning the object key it was stored under
    """
    bucket = bucket or os.environ["AWS_S3_BUCKET"]
    key = key or filepath.rpartition("/")[2]

    client = get_client()
    client.upload_file(filepath, bucket, key)
    return key


def delete_file(key, bucket=None):
    """
    Delete an object from S3
    """
    bucket = bucket or os.environ["AWS_S3_BUCKET"]

    client = get_client()
    client.delete_object(Bucket=bucket, Key=key)
    return key
