import boto3
from botocore.exceptions import NoCredentialsError
import json
import os

def dump_to_cloudflare_r2(all_batch_results, access_key, secret_key, bucket_name, file_name, signature_record_file):
    # Initialize the S3 client
    s3_client = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key, endpoint_url='https://37a4fe05d373bdc73551b5386c2c4cb3.r2.cloudflarestorage.com')

    # Load existing signatures from the record file
    if os.path.exists(signature_record_file):
        with open(signature_record_file, 'r') as file:
            existing_signatures = set(json.load(file))
    else:
        existing_signatures = set()

    new_batch_results = []
    new_signatures = set()

    # Filter out transactions with signatures already in the record
    for result in all_batch_results:
        signature = result['transaction']['signatures'][0] if result['transaction']['signatures'] else None
        if signature and signature not in existing_signatures:
            new_batch_results.append(result)
            new_signatures.add(signature)

    if new_batch_results:
        try:
            # Convert new batch results to JSON
            batch_data = json.dumps(new_batch_results)

            # Upload the data to Cloudflare R2
            s3_client.put_object(Bucket=bucket_name, Key=file_name, Body=batch_data)
            print(f"Uploaded {file_name} to Cloudflare R2 bucket {bucket_name}")

            # Update the record file
            existing_signatures.update(new_signatures)
            with open(signature_record_file, 'w') as file:
                json.dump(list(existing_signatures), file)

        except NoCredentialsError:
            print("Credentials not available")
    else:
        print("No new transactions to upload")