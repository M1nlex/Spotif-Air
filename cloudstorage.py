"""Programatically interact with a Google Cloud Storage bucket."""

from pip._internal import main as pipmain
from os import environ
import os

try:
    from google.cloud import storage
except ModuleNotFoundError:
    pipmain(['install', 'google-cloud-storage'])
    from google.cloud import storage

bucketName = environ.get('spotifair')
bucketFolder = environ.get('Song')
localFolder = environ.get('file')

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "Spotifair-df3788c7a929.json"
storage_client = storage.Client()
bucket = storage_client.get_bucket('spotifair')

def upload_files(bucketName, bucketFolder, localFolder, name):
    """Upload files to GCP bucket."""
    blob = bucket.blob(bucketFolder +'/' + name)
    blob.upload_from_filename(localFolder + name)
    return f'Uploaded {name} to "{bucketName}" bucket.'

def list_files(bucketName):
    """List all files in GCP bucket."""
    files = bucket.list_blobs(prefix=bucketFolder)
    fileList = [file.name for file in files if '.' in file.name]
    return fileList


def download_random_file(bucketName, bucketFolder, localFolder, name):
    """Download random file from GCP bucket."""
    fileList = list_files(bucketName)

    for i in range(len(fileList)):
        #print(fileList[i], str(name))
        if fileList[i] == str(name):
            song = i
            break

    blob = bucket.blob(fileList[song])
    fileName = blob.name.split('/')[-1]
    blob.download_to_filename(localFolder + fileName)
    return f'{fileName} downloaded from bucket.'
