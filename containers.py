import time

import boto3
import docker
from botocore.exceptions import ClientError

from settings import Settings


settings = Settings()
docker_c = docker.from_env()

containers = {
    "minio": {
        "name": "minio",
        "image": "quay.io/minio/minio:latest",
        "command": 'server /data --console-address ":9001"',
        "environment": {
            "MINIO_ROOT_USER": "miniodev",
            "MINIO_ROOT_PASSWORD": "miniodev",
        },
        "volumes": ["/Users/musatai/code/midas/minio-storage:/data"],
        "ports": {
            "9000": 9000,
            "9001": 9001,
        },
        "network": "midas",
    },
    "dynamodb": {
        "name": "dynamodb",
        "image": "amazon/dynamodb-local:latest",
        "command": "-jar DynamoDBLocal.jar -sharedDb -dbPath /home/dynamodblocal/data/",
        "environment": {
            "MINIO_ROOT_USER": "miniodev",
            "MINIO_ROOT_PASSWORD": "miniodev",
        },
        "volumes": [
            "/Users/musatai/code/midas/dynamodb-storage:/home/dynamodblocal/data"
        ],
        "ports": {
            "8000": 8000,
        },
        "network": "midas",
    },
    "midas-news-parser": {
        "name": "midas-news-parser",
        "image": "midas/news-parser:0.1.0",
        "environment": {
            "RUN_ID": settings.RUN_ID,
            "BUCKET": settings.BUCKET,
            "NEWS_KEYWORDS": settings.NEWS_KEYWORDS,
            "NEWS_API_KEY": settings.NEWS_API_KEY,
        },
        "network": "midas",
    },
    "midas-news-scorer": {
        "name": "midas-news-scorer",
        "image": "midas/news-scorer:0.1.0",
        "environment": {
            "RUN_ID": settings.RUN_ID,
            "BUCKET": settings.BUCKET,
            "NEWS_KEYWORDS": settings.NEWS_KEYWORDS,
            "OPENAI_API_KEY": settings.OPENAI_API_KEY,
        },
        "network": "midas",
    },
    "midas-heuristic-scorer": {
        "name": "midas-heuristic-scorer",
        "image": "midas/heuristic-scorer:0.1.0",
        "environment": {
            "RUN_ID": settings.RUN_ID,
            "BUCKET": settings.BUCKET,
        },
        "network": "midas",
    },
    "bifrost-data-bridge": {
        "name": "bifrost-data-bridge",
        "image": "midas/bifrost-data-bridge:0.1.0",
        "environment": {
            "RUN_ID": settings.RUN_ID,
            "BUCKET": settings.BUCKET,
        },
        "network": "midas",
    },
}


def configure_minio() -> None:
    _s3 = boto3.resource(
        "s3",
        endpoint_url="http://localhost:9000",
        aws_access_key_id="miniodev",
        aws_secret_access_key="miniodev",
        verify=False,
    )

    try:
        buckets = [bucket.name for bucket in _s3.buckets.all()]
        if settings.BUCKET not in buckets:
            _s3.create_bucket(Bucket=settings.BUCKET)
    except ClientError as err:
        raise ClientError from err


def wait_for_container(name: str) -> None:
    while True:
        status = docker_c.containers.get(name).status
        if status == "exited":
            break
        time.sleep(1)
