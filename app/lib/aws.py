import boto3
import uuid
import os 

from flask import current_app
from werkzeug.datastructures.file_storage import FileStorage


def upload_proof_of_death(file: FileStorage) -> str | None:
    """
    Function that uploads a proof of death file to S3, with a UUID as the filename.
    """
    file_extension = os.path.splitext(file.filename)[1]

    filename = str(uuid.uuid4()) + file_extension
    
    return upload_file_to_s3(file=file, bucket_name=current_app.config["PROOF_OF_DEATH_BUCKET_NAME"], filename_override=filename)


def upload_file_to_s3(file: FileStorage, bucket_name: str, filename_override: str | None = None) -> str | None:
    """
    Generic function that takes a file and uploads it to a given S3 bucket.
    """
    if file:
        s3 = boto3.client(
            "s3",
            aws_access_key_id=current_app.config["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=current_app.config["AWS_SECRET_ACCESS_KEY"],
            aws_session_token=current_app.config.get("AWS_SESSION_TOKEN"),
            region_name=current_app.config.get("AWS_DEFAULT_REGION", "eu-west-2"),
        )

        filename = filename_override if filename_override else file.filename

        try:
            s3.upload_fileobj(file, bucket_name, filename)
        except Exception as e:
            current_app.logger.error(f"Error uploading file to S3: {e}")
            return None

        return filename