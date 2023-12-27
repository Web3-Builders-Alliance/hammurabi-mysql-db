import os
import boto3
from dotenv import load_dotenv
from botocore.exceptions import NoCredentialsError

def upload_to_r2(file_name, bucket, object_name=None):
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Set up a session with your R2 credentials
    session = boto3.session.Session()
    s3_client = session.client(
        service_name='s3',
        endpoint_url=os.getenv('CLOUDFLARE_API'),  
        aws_access_key_id=os.getenv('CLOUDFLARE_ACCESS_KEY'),         
        aws_secret_access_key=os.getenv('CLOUDFLARE_SECRET_KEY')     
    )

    # Upload the file
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except NoCredentialsError:
        print("Credentials not available")
        return False
    return True

# Example usage
upload_to_r2('test.jpg', 'orca-sol-usdc')
