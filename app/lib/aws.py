
import boto3
import uuid

from flask import current_app

def file_upload_to_proof_of_death_storage(file) -> str | None:
    if file:
        s3 = boto3.client(
            "s3",
            aws_access_key_id=current_app.config["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=current_app.config["AWS_SECRET_ACCESS_KEY"],
            region_name=current_app.config.get("AWS_REGION", "eu-west-2"),
        )
        bucket_name = current_app.config["S3_BUCKET_NAME"]
        
        filename = str(uuid.uuid4())
        
        s3.upload_fileobj(file, bucket_name, filename)

        return filename