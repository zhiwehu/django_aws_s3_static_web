try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO

import mimetypes
import zipfile

from boto.s3.connection import S3Connection

from .settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY


def connect_aws_s3(key=None, secret=None):
    if not key:
        key = AWS_ACCESS_KEY_ID
    if not secret:
        secret = AWS_SECRET_ACCESS_KEY
    conn = S3Connection(key, secret)
    return conn


def create_bucket(conn, bucket_name):
    return conn.create_bucket(bucket_name, policy='public-read')


def push_file_to_s3(bucket, file_name, content):
    """
    Save file.
    """
    key = bucket.new_key(file_name)
    content.seek(0)

    try:
        content_type = mimetypes.guess_type(file_name)[0]
        if content_type:
            key.set_metadata('Content-Type', content_type)
        key.set_contents_from_file(content)
    except Exception as e:
        raise IOError('Error during uploading file %s - %s' % (file_name, e.message))

    content.seek(0, 2)
    orig_size = content.tell()
    saved_size = key.size

    if saved_size == orig_size:
        key.set_acl('public-read')
    else:
        key.delete()

        raise IOError('Error during saving file %s - saved %s of %s bytes'
                      % (file_name, saved_size, orig_size))

    return file_name


def fileiterator(zip_file):
    with zipfile.ZipFile(zip_file, "r", zipfile.ZIP_STORED) as openzip:
        filelist = openzip.infolist()
        for f in filelist:
            if f.file_size:
                yield (f.filename, openzip.read(f))


def upload_zip_file_s3(bucket, zip_file):
    for filename, content in fileiterator(zip_file):
        content_string = StringIO()
        content_string.write(content)
        push_file_to_s3(bucket, filename, content_string)
