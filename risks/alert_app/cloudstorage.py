"""Module to write to google cloud storage"""
import os
from google.cloud import storage

bucket_name = os.environ.get('RISK_BUCKET_NAME')
google_cloud_project = os.environ['GOOGLE_CLOUD_PROJECT']


def upload_blob(blob_name, blob_data):
    """Uploads a file to the bucket."""
    storage_client = storage.Client(project=google_cloud_project)
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_string(blob_data)


def download_blob(blob_name):
    """Downloads a blob from the bucket."""
    storage_client = storage.Client(project=google_cloud_project)
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)
    return blob.download_as_string()
