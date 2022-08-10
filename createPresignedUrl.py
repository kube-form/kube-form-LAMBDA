import json
import boto3
from botocore.exceptions import ClientError

def create_presigned_url(bucket_name, object_name, expiration=600):

    # Generate a presigned URL for the S3 object
    s3_client = boto3.client('s3',region_name="ap-northeast-2",config=boto3.session.Config(signature_version='s3v4',))
    try:
        url = s3_client.generate_presigned_url('put_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except Exception as e:
        print(e)
        return "Error"

    # The response contains the presigned URL
    return url
    

def lambda_handler(event, context):
    print(event['objectKey'] + "!!!!")
    url = create_presigned_url('kube-form','dockerImages/' + event['objectKey'], 7200)
    return {
        "status" : 200,
        "url" : url
    }