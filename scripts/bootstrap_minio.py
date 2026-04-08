from minio import Minio
from app.core.config import settings

client = Minio(settings.minio_endpoint, access_key=settings.minio_access_key, secret_key=settings.minio_secret_key, secure=False)
if not client.bucket_exists(settings.minio_bucket):
    client.make_bucket(settings.minio_bucket)
    print(f"Created bucket {settings.minio_bucket}")
else:
    print(f"Bucket already exists: {settings.minio_bucket}")
