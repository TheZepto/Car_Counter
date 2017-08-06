import os
import sys
import threading

import boto3


class S3Bucket:
    """Connect to an S3 bucket and provides a method
    for uploading a fileobj to it.
    """
    def __init__(self, bucket):
        # Initialise the s3 connection
        s3 = boto3.resource('s3')
        # Check that the bucket exists and is accessible to IAM user
        s3.meta.client.head_bucket(Bucket=bucket)

        self.bucket = s3.Bucket(bucket)

    def uploadstream(self, buffer, name):
        # Need to seek to end of stream and tell to find size
        buffer.seek(0, os.SEEK_END)
        size = buffer.tell()
        buffer.seek(0)

        self.bucket.upload_fileobj(
            Fileobj=buffer,
            Key=name,
            Callback=ProgressPercentageStream(name, size)
        )


class ProgressPercentageStream(object):
    """Callback function for providing upload percentage of single file."""
    def __init__(self, filename, size):
        self._filename = filename
        self._size = size
        self._seen_so_far = 0
        self._lock = threading.Lock()

    def __call__(self, bytes_amount):
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self._size) * 100
            sys.stdout.write(
                "\r%s  %s / %s  (%.2f%%)" % (
                    self._filename, self._seen_so_far, self._size,
                    percentage))
            sys.stdout.flush()