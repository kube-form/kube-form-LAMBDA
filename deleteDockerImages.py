import json
import boto3

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('DockerImages')

    response = table.delete_item(
        Key = {
            'id': int(event['params']['path']['id'])
        }
    )
	
    return {
        'statusCode': 200,
        'body': response
    }
