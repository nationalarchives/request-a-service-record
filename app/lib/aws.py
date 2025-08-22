import boto3
import uuid
import os 

from flask import current_app
from werkzeug.datastructures.file_storage import FileStorage

def upload_file_to_s3(file: FileStorage, bucket_name: str) -> str | None:
    if file:
        s3 = boto3.client(
            "s3",
            aws_access_key_id=current_app.config["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=current_app.config["AWS_SECRET_ACCESS_KEY"],
            aws_session_token=current_app.config.get("AWS_SESSION_TOKEN"),
            region_name=current_app.config.get("AWS_DEFAULT_REGION", "eu-west-2"),
        )

        file_extension = os.path.splitext(file.filename)[1]

        filename = str(uuid.uuid4()) + file_extension

        try:
            s3.upload_fileobj(file, bucket_name, filename)
        except Exception as e:
            current_app.logger.error(f"Error uploading file to S3: {e}")
            return None

        return filename