import json
import boto3

client = boto3.client('glue')

glue_job_name = "external_data_copy"

def lambda_handler(event, context):

    bucket_name = event['Records'][0]['s3']['bucket']['name']
    file_key = event['Records'][0]['s3']['object']['key']
    source_path = f's3://{bucket_name}/{file_key}'
    destination_folder = file_key.split('/')[0]
    destination_path = f's3://arindam-s3-bucket-all-purpose/external-data-raw-layer/{destination_folder}'

    client.start_job_run(
    JobName = glue_job_name,
    Arguments = {
        '--S3_Source_Path': source_path,
        '--S3_Destination_Path': destination_path
    }
    )