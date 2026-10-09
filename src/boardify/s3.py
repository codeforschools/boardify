import boto3


def get_bucket(cfg):
    bucket = cfg.get("pdf_bucket")
    if not bucket:
        raise SystemExit("pdf_bucket is not set in [tool.boardify] (the bucket PDFs are uploaded to).")
    return bucket


def get_client(cfg):
    """
    S3 client in the configured region. Credentials come from boto3's default chain
    (an OIDC role in CI, an AWS profile locally); no long-lived keys are read.
    """
    return boto3.client("s3", region_name=cfg.get("pdf_region") or None)


def upload_file(cfg, filepath, key=None):
    """
    Upload a local PDF to S3, returning the object key it was stored under
    """
    key = key or filepath.rpartition("/")[2]
    get_client(cfg).upload_file(
        filepath, get_bucket(cfg), key, ExtraArgs={"ContentType": "application/pdf"}
    )
    return key


def delete_file(cfg, key):
    """
    Delete an object from S3
    """
    get_client(cfg).delete_object(Bucket=get_bucket(cfg), Key=key)
    return key
