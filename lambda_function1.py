import json
import urllib.parse
import boto3

# Initialize the AWS Glue client outside the handler to make it faster
client = boto3.client('glue')

glue_job_name = "external_data_copy"

def lambda_handler(event, context):
    try:
        # 1. Safely extract bucket name and raw file key
        bucket_name = event['Records'][0]['s3']['bucket']['name']
        raw_file_key = event['Records'][0]['s3']['object']['key']
        
        # 2. FIX: Decode the file name to handle spaces (+) and special characters
        file_key = urllib.parse.unquote_plus(raw_file_key)
        
        # 3. Create the exact source path
        source_path = f's3://{bucket_name}/{file_key}'
        
        # 4. FIX: Extract the folder path safely, even for deeply nested folders
        # This removes the file name from the end and keeps the whole folder path
        if '/' in file_key:
            destination_folder = file_key.rsplit('/', 1)[0]
            destination_path = f's3://arindam-s3-bucket-all-purpose/external-data-raw-layer/{destination_folder}/'
        else:
            # File was uploaded directly to the root of the bucket (no folders)
            destination_path = 's3://arindam-s3-bucket-all-purpose/external-data-raw-layer/'
            
        print(f"Triggered by: {source_path}")
        print(f"Sending target folder to Glue: {destination_path}")

        # 5. Start the AWS Glue Job
        response = client.start_job_run(
            JobName=glue_job_name,
            Arguments={
                '--S3_Source_Path': source_path,
                '--S3_Destination_Path': destination_path
            }
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps(f"Glue job started successfully. Run ID: {response['JobRunId']}")
        }
        
    except Exception as e:
        print(f"Error triggering Glue Job: {str(e)}")
        raise e
