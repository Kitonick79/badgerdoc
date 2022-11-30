from src import config


def tenant_from_bucket(bucket: str) -> str:
    prefix = f"{config.S3_PREFIX}-" if config.S3_PREFIX else ""
    return bucket.replace(prefix, "", 1)
