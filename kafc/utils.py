import boto3
import io
from typing import BinaryIO


class ManageFile:
    """
    It's class for performing collaboration with aws:s3 technology
    """
    def __init__(self, bucket_name: str, aws_access_key_id: str, aws_secret_access_key: str) -> None:
        self.bucket_name = bucket_name
       
        self.client = boto3.client("s3", aws_access_key_id=aws_access_key_id,
                                         aws_secret_access_key=aws_secret_access_key)


    def upload_file(self, file: BinaryIO, filename: str) -> str:
        self.client.upload_fileobj(file, self.bucket_name, filename)

    def download_file(self, filename: str) -> BinaryIO:
        file = io.BytesIO()
        self.client.download_fileobj(self.bucket_name, filename, Fileobj=file)
        file.seek(0)
        return file

    def drop_file(self, filename: str) -> None:
        self.client.delete_object(Bucket=self.bucket_name, Key=filename)





