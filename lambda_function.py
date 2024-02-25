import boto3
import os
import zipfile

s3 = boto3.client('s3')

def lambda_handler(event, context):
    # Get the bucket name and object key from the event
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    object_key = event['Records'][0]['s3']['object']['key']
    
    # Create a temporary directory to store the compressed file
    temp_dir = '/tmp'
    file_name = os.path.basename(object_key)
    zip_file_path = os.path.join(temp_dir, file_name + '.zip')
    
    # Download the object to local storage
    local_file_path = os.path.join(temp_dir, file_name)
    s3.download_file(bucket_name, object_key, local_file_path)
    
    # Compress the object into a ZIP file
    with zipfile.ZipFile(zip_file_path, 'w') as zipf:
        zipf.write(local_file_path, file_name)
    
    # Upload the compressed file back to S3
    s3.upload_file(zip_file_path, bucket_name, file_name + '.zip')
    
    # Delete the original object from S3
    s3.delete_object(Bucket=bucket_name, Key=object_key)
    
    return {
        'statusCode': 200,
        'body': 'Object compressed and uploaded successfully.'
    }
