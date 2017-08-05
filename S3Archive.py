import os
import tarfile
import datetime
from io import BytesIO

import boto3


class S3Archive:
    def __init__(
        self,
        archive_name,
        bucket_name,
        add_datetime_to_name=True,
    ):
        self.bucket_name = bucket_name

        if add_datetime_to_name:
            time_now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            archive_name += time_now
        self.archive_name = archive_name + '.tar'

        self.files_for_archive = []

    def addfile(
        self,
        file_location
    ):
        if os.path.isfile(file_location):
            self.files_for_archive.append(file_location)
        else:
            raise(FileNotFoundError)

    def __makearchive( 
        self
    ):
        archive_in_ram = BytesIO()
        with tarfile.open(fileobj=archive_in_ram, mode='w:gz') as tar_file:
            for fname in self.files_for_archive:
                tar_file.add(name=fname)
            tar_file.close()

        archive_in_ram.seek(0)  # <--- reset your cursor

        print("Archive written with {} files".
              format(len(self.files_for_archive))
              )
        return archive_in_ram

    def create(
        self
    ):
        archive = self.__makearchive()

        s3 = boto3.resource('s3')
        print("Starting upload to S3 bucket: " + self.bucket_name)
        s3.Object(self.bucket_name, self.archive_name).put(Body=archive.read())
        print("Finished upload of " + self.archive_name)
