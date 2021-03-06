# to access Amazon S3
import boto3
from configs3 import S3_KEY, S3_SECRET_ACCESS_KEY, S3_BUCKET
from flask import session


def get_s3_resource():
    if S3_KEY and S3_SECRET_ACCESS_KEY:
        return boto3.resource('s3',
                              aws_access_key_id=S3_KEY,
                              aws_secret_access_key=S3_SECRET_ACCESS_KEY
                              )

    else:
        return boto3.resource('s3')


def get_s3_client():
    if S3_KEY and S3_SECRET_ACCESS_KEY:
        return boto3.client('s3',
                              aws_access_key_id=S3_KEY,
                              aws_secret_access_key=S3_SECRET_ACCESS_KEY
                              )

    else:
        return boto3.client('s3')


def get_bucket():
    s3_resource = get_s3_resource()
    if 'bucket' in session:
        bucket = session['bucket']
    else:
        bucket = S3_BUCKET
    return s3_resource.Bucket(bucket)


def get_bucket_list():
    client = boto3.client('s3')
    return client.list_buckets().get("Buckets")
