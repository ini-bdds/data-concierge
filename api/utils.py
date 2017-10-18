import os
import json
import uuid
import boto3
from minid_client import minid_client_api
from bdbag import bdbag_api

from app import app

def create_bag_archive(metadata):
    bag_name = "/tmp/bag_tmp/%s" % str(uuid.uuid4())
    metadata_file = "/tmp/bag_tmp/%s" % str(uuid.uuid4())
    with open(metadata_file, 'w') as f:
        f.write(json.dumps(metadata))

    os.mkdir(bag_name)
    bdbag_api.make_bag(bag_name,
                   algs=['md5', 'sha256'],
                   metadata={'Creator-Name': 'Encode2BDBag Service'},
                   remote_file_manifest=metadata_file
                   )
    bdbag_api.archive_bag(bag_name, app.config['BAG_ARCHIVE_FORMAT'])

    archive_name = '{}.{}'.format(bag_name,app.config['BAG_ARCHIVE_FORMAT'])
    bdbag_api.revert_bag(bag_name)
    os.remove(metadata_file)
    return archive_name


def create_minid(filename, aws_bucket_filename):
    checksum = minid_client_api.compute_checksum(filename)
    return minid_client_api.register_entity(app.config['MINID_SERVER'],
                                         checksum,
                                         app.config['MINID_EMAIL'],
                                         app.config['MINID_CODE'],
                                         ["https://s3.amazonaws.com/%s/%s.zip" % (app.config['BUCKET_NAME'], aws_bucket_filename)],
                                         "ENCODE BDBag",
                                         app.config['MINID_TEST'])


def upload_to_s3(filename, key):
    s3 = boto3.resource('s3', aws_access_key_id=app.config['AWS_ACCESS_KEY_ID'], aws_secret_access_key=app.config['AWS_SECRET_ACCESS_KEY'])
    data = open(filename, 'rb')
    s3.Bucket(app.config['BUCKET_NAME']).put_object(Key=key, Body=data)


